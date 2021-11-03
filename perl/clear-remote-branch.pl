#!/usr/bin/env perl
package main;
use strict;
use warnings FATAL => 'all';
use Getopt::Long; # 文档: https://perldoc.perl.org/Getopt::Long
use Pod::Usage; # 文档 https://perldoc.perl.org/Pod::Usage


# 注意, 此脚本只会删除远程分支, 不会删除本地分支
# 指定远程名称
my $remoteName = 'origin';
my $remoteBranchName = 'master';
my $help = 0;
my @filterBranchName = ();
my $test = 0;
my $delLocal = 0;
my $prefix = '';
my $outputFile = '';
my $quit = 0;

my $optionIsOk = GetOptions ("remote=s" => \$remoteName,
    "branch=s" => \$remoteBranchName,
    "filter=s{1,}" => \@filterBranchName,
    "output=s" => \$outputFile,
    "quit" => \$quit,
    "local" => \$delLocal,
    "test" => \$test,
    "prefix=s" => \$prefix,
    "help|?" => \$help);
# 参数错误
pod2usage(2) if $optionIsOk != 1;
# 输出帮助文档
pod2usage(1) if $help != 0;

# 默认过滤的分支
if(@filterBranchName == 0){
    @filterBranchName = ('master', 'sim_master', 'sim_default', 'dev');
}

`git checkout $remoteBranchName > - 2>&1`;
`git pull > - 2>&1`;
`git fetch --all > - 2>&1`;
# 获取所有已经合并到master的分支列表
my $allMergedBranchStr = `git branch -a --merged $remoteBranchName`;
my @allMergedBranch = split(/\n/, $allMergedBranchStr);
foreach my $item (@allMergedBranch) {
    # 去掉前后空格
    $item =~ s/^\s+|\s+$//g;
    # 判断当前分支是否需要处理
    my $isFilter = 0;
    # 本地分支过滤
    if(!($item =~ /^remotes\/$remoteName/)){
        $isFilter = 1;
    }
    # 特定分支过滤
    foreach my $filterBranch (@filterBranchName){
        if($item eq $filterBranch) {
            $isFilter = 1;
        }elsif($item eq "remotes/$remoteName/$filterBranch"){
            $isFilter = 1;
        }
    }
    # HEAD 指针过滤
    if($item =~ /HEAD/){
        $isFilter = 1;
    }
    if($isFilter == 1) {next;}
    # 获取分支名
    my $branchName =  $item;
    $branchName =~ s/remotes\/$remoteName\///;
    # 判断分支前缀
    if($prefix ne '' && !($branchName =~ /^$prefix/)){
        next;
    }
    # 获取git的最新一次commit id
    # 将其打印, 防止删错分支还可以恢复
    my $newestCommitId = `git rev-parse $remoteName/$branchName`;
    $newestCommitId =~ s/^\s+|\s+$//g;
    if($quit == 0){
      print($branchName);
      print("\n");
      print($newestCommitId);
      print("\n");
    }
    # 将内容进行记录
    if($outputFile ne ''){
        `echo "$branchName" >> $outputFile`;
        `echo "$newestCommitId" >> $outputFile`;
    }
    # 删除远程分支
    if($test == 0) {
        `git push $remoteName --delete $branchName > - 2>&1`;
        if($delLocal != 0) {
            `git branch -d $branchName > - 2>&1`;
        }
    }
}

__END__

=head1 SYNOPSIS

clear-remote-branch.pl [options]

将远程所有已经合并到 master 的分支删除.

脚本在删除的时候, 会将删除的分支以及分支指针所指向的 commit_id 进行打印.
若需要恢复数据可自行保存

为脚本创建可执行软连接:

ln -s <完整路径>/clear-remote-branch.pl /usr/local/bin/clear-remote-branch


Options:

   --remote|-r          远程 remote 名称 (origin)
   --branch|-b          基准分支 (master)
   --filter|-f          指定需要过滤的分支 (master, sim_master, sim_default, dev)
                    --filter branch1 branch2 branch3
   --local|-l           同步删除本地分支
   --prefix|-p          添加分支的前缀判断
   --test|-t            脚本测试, 只打印要删除的分支, 不执行删除逻辑
   --output|-o          将内容追加到文件中
   --quit|-q            静默清除
   --help|-h            打印帮助文档
=cut
