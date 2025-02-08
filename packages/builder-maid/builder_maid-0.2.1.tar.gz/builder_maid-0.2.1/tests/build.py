from builder_maid import target

t = target()

t.set_compiler("gcc")
t.add_files("main.cpp")
t.add_flags("-std=c++20")
t.add_flags("-lstdc++")
t.compile("main.out")
