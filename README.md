用来存放一些小工具

# bash

## reanme_file_md5

将目录下的所有文件使用 md5 重命名. 

初始的需求是为了将重复的文件去掉

# Python

可通过修改文件`.bash_profile`来自定义命令: 

```shell
alias command="python3 /path/xxx/main.py"
```

## project_note_translation 

将项目中所有的英文注释转成中文

不知道你有没有和我一样的烦恼, 自己的英文不好, 但是阅读一些开源框架的时候, 所有的注释又都是用英文书写的, 边看边翻译, 导致阅读进度极慢. 

这个工具可以将项目中所有的英文注释翻译成中文后, 原样输出一个拷贝项目

## markdown_to_epub

将 markdown 装换为 epub 电子书形式

# perl

## clear-remote-branch.pl

在平常开发过程中, 每次新任务都要拉新的分支出去. 这个任务分支等到合并到`master`之后, 也就没有用了. 

此脚本可将所有已经合并到`master`的远程分支删除