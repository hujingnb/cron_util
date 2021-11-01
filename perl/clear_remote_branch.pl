#!/usr/bin/env perl
package main;
use strict;
use warnings FATAL => 'all';

# 注意, 此脚本只会删除远程分支, 不会删除本地分支
# 指定远程名称
my $remoteName = 'origin';
my $remoteBranchName = 'master';

`git checkout master > - 2>&1`;
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
    foreach my $filterBranch ('master', 'sim_master', 'sim_default', 'dev'){
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
    # 获取git的最新一次commit id
    # 将其打印, 防止删错分支还可以恢复
    my $newestCommitId = `git rev-parse $remoteName/$branchName`;
    print($branchName);
    print("\n");
    print($newestCommitId);
    print("\n");
    # 删除远程分支
    `git push $remoteName --delete $branchName > - 2>&1`;
}