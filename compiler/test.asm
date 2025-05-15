pointer (x) = 0xffff
label a:
    jmp label(a)
    # Regular instructions
    add reg0,reg1,reg2
    nop
    inc reg0
    store {"ola"} x
    store {'a'} in 0xfafc
    pointer (mario) = 0xcccc
    store {0b0000000000000000,0b0000000000000001,0b0000000000000011} in mario
