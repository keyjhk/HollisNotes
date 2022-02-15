import os,re

ISCODE=False
ADD=None
NUM=None


def title_update(x):
    if ADD=='+':
        res=x.group(1)+'#'*NUM +x.group(2)
    else:
        res=x.group(1)[:-int(NUM)] + x.group(2)
    print('原来的字符串：%s 修改后的字符串：%s' % (x.group(0),res))

    return res


if __name__ == '__main__':
    files=[]
    for idx,file in enumerate(os.listdir()):
        print('%s. %s' % (idx,file))
        files.append(file)
    choice=int(input())
    title_command = input('ex:+1(标题#+1)')
    ADD=title_command[0]
    NUM=title_command[1]

    with open('test.md','r',encoding='utf8') as f,\
            open('out.md','w',encoding='utf8') as f1:
        title_re=r'(#+)(\s\w+)'
        for line in f:
            # print(line)
            if '```' in line:ISCODE=not ISCODE # 代码块
            if ISCODE:
                f1.write(line)
                continue

            line=re.sub(title_re,title_update,line)
            f1.write(line)

