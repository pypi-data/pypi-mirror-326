from builder_maid import target

t = target("gcc")

t.set_compiler("gcc")
t.add_files("main.cpp")
t.add_flags("-std=c++20")
t.add_flags("-lstdc++")
print(t.get_command())
t.compile("main.out")
