pointer (x) = 0xffff
label a:
    jmp label(a)
    # Regular instructions
    add reg0,reg1,reg2
    nop
    inc reg0
    store {"ola"} in x
    store {'a'} 0xfafc
    pointer (mario) = 0xcccc
    store {0000000000000000,0000000000000001,0000000000000011} in mario
