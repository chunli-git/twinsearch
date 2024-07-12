from descriptor import glcm, bitdesc

path = 'images/test.png'
patha = 'images/testa.png'
pathb = 'images/testb.png'

def main():
    feat_glcm = glcm(path)
    print(f'GLCM\n-----\n{feat_glcm}')
    feat_bit = bitdesc(path)
    print(f'Bitdesc\n--------\n{feat_bit}')

    
if __name__ == '__main__':
    main()