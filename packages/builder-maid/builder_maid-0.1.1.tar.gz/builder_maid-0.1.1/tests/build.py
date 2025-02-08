from builder_maid import target

t = target.target()

t.add_files("main.cpp")
t.compile("main.out")
