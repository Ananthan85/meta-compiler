import sys, os, subprocess

def compile_poly(filepath):
    with open(filepath, 'r') as f:
        data = f.read()

    try:
        # fixed the parser to handle any order of @c and @go
        if data.find("@c") < data.find("@go"):
            c_part = data.split("@c")[1].split("@go")[0].strip()
            go_part = data.split("@go")[1].strip()
        else:
            go_part = data.split("@go")[1].split("@c")[0].strip()
            c_part = data.split("@c")[1].strip()
    except:
        sys.exit("err: check tags")

    with open("tmp_c.c", "w") as f: f.write(c_part)
    with open("tmp_go.go", "w") as f: f.write(go_part)

    # c side frontend
    subprocess.run(["clang", "-S", "-emit-llvm", "-O0", "tmp_c.c", "-o", "c.ll"], check=True)
    
    # go side frontend
    env = os.environ.copy()
    env["GOROOT"] = "/home/feyd/sdk/go1.22.12"
    env["PATH"] = "/home/feyd/sdk/go1.22.12/bin:" + env["PATH"]
    env["CGO_ENABLED"] = "1"
    
    subprocess.run([
        "tinygo", "build", 
        "-opt=0", 
        "-o", "go.ll", 
        "-scheduler=none", 
        "-gc=leaking",
        "-panic=trap", 
        "tmp_go.go"
    ], env=env, check=True)

    # linking phase
    subprocess.run(["llvm-link", "-S", "c.ll", "go.ll", "-o", "unified.ll"], check=True)

    # backend
    subprocess.run([
        "llc", 
        "-relocation-model=pic", 
        "-filetype=obj", 
        "unified.ll", 
        "-o", "final.o"
    ], check=True)

    bin_name = filepath.split('.')[0]
    try:
        subprocess.run(["clang", "final.o", "-o", bin_name, "-no-pie"], check=True)
    except:
        subprocess.run(["clang", "final.o", "-o", bin_name], check=True)

    # cleanup
    for f in ["tmp_c.c", "tmp_go.go", "c.ll", "go.ll", "unified.ll", "final.o"]:
        if os.path.exists(f): os.remove(f)

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    compile_poly(sys.argv[1])
