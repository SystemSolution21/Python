def scope_test():
    spam = "test_non_local"

    def local_scope():
        spam = "local_spam"
        return spam

    def non_local_scope():
        nonlocal spam
        spam = "non_local_spam"
        return spam

    def global_scope():
        global spam
        spam = "global_spam"
        return spam

    print(f"{local_scope()= } >>", spam)
    print(f"{non_local_scope()= } >>", spam)
    print(f"{global_scope()= } >>", spam)


spam = "test_global"
scope_test()
print("In global scope:", spam)
