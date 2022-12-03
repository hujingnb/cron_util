#!/usr/bin/env bash

dir=$1
# 传递
if [ -z "$dir" ]; then
    echo "将路径下的所有文件使用 md5 重命名. 请指定路径"
    exit 1
fi
# 安装 brew install md5sha1sum
for file in "$dir"/*; do
  echo $file
  md5=$(md5 "${file}" | awk '{print $NF}')
  # 获取文件后缀
  suffix=$(echo "$file" | rev | cut -d . -f 1 | rev)
  # 重命名
  mv "$file" "$dir/$md5.$suffix"
done


