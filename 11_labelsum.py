import glob,argparse,os,shutil

def parse_args():
    parser = argparse.ArgumentParser(description='Count pedestrains from each camera to a txt file.')
    parser.add_argument('--root', dest='root',required=True, help='path to root')
    parser.add_argument('--id', dest='id', required=True, help='which id to extract')
    parser.add_argument('--target', dest='target', help='which id to extract',default='results.txt')
    args = parser.parse_args()
    return args

if __name__ =='__main__':
    args = parse_args()
    folders = glob.glob(os.path.join(args.root, '{}*'.format(args.id)))
    target = os.path.join(args.root,args.target)
    if os.path.exists(target):
        os.remove(target)

    for folder in folders:
        if not os.path.isdir(folder):
            continue
        if '\\' in folder:	
            sep = '\\'
        else:
            sep = '/'
        ims= glob.glob(folder+'{}*.jpg'.format(sep))
        dict = {}
        dict1 = {}
        with open(target, 'a') as f:
            
            for im in ims:
                name = im.split(sep)[-1]
                cam = name.split('_')[0]
                num = dict.get(cam,0)
                dict[cam] = num+1
            print(folder)
            f.write('\n'+folder.split(sep)[-1]+': \t{}\t{}'.format(len(ims),len(dict.keys())))

            for key in dict.keys():
                f.write('\t{}\t{}'.format(key, dict[key]))
            
    with open(os.path.join(args.root,'counts.txt'),'w') as fc:
            with open(target,'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.rstrip() == '':
                        continue
                    id = line.split('\t')[0]
                    #print(id)
                    num = line.split('\t')[1]
                    #print(num)
                    cams = int(line.split('\t')[2])
                    #print(cams)
                    num = dict1.get(cams,0)
                    dict1[cams] = num + 1

                for key in sorted(dict1.keys()):
                    fc.write('cross {} camers has {} ids\n'.format(key,dict1[key]))
