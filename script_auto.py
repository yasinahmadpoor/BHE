import os
for f in os.listdir(r'D:\test_auto'):
    path_ = r'D:\test_auto\{}'.format(f)
    os.chdir(path_)
    os.system('cmd /c "ogs 3D_deep_BHE_CXA.prj"')
