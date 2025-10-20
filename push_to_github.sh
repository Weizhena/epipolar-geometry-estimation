#!/bin/bash

echo "=========================================="
echo "GitHub 推送脚本 / GitHub Push Script"
echo "=========================================="
echo ""
echo "作者 / Author: weizhena"
echo "项目 / Project: Epipolar Geometry & Fundamental Matrix Estimation"
echo ""
echo "请先在 GitHub 创建仓库，然后将仓库 URL 填入下方："
echo "Please create a GitHub repository first, then enter the URL below:"
echo ""
echo "示例 / Example: https://github.com/weizhena/epipolar-geometry-estimation.git"
echo ""
echo "推荐仓库名 / Recommended names:"
echo "  - epipolar-geometry-estimation"
echo "  - fundamental-matrix-estimation"
echo "  - cv-experiment4"
echo ""

read -p "请输入 GitHub 仓库 URL / Enter GitHub repo URL: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "错误: 仓库 URL 不能为空 / Error: Repository URL cannot be empty"
    exit 1
fi

echo ""
echo "正在添加远程仓库 / Adding remote repository..."
git remote add origin "$REPO_URL" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "远程仓库已存在，更新 URL / Remote already exists, updating URL..."
    git remote set-url origin "$REPO_URL"
fi

echo "正在推送到 GitHub / Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ 成功推送到 GitHub! / Successfully pushed!"
    echo "=========================================="
    echo ""
    echo "你的仓库地址 / Your repository: $REPO_URL"
    echo ""
    echo "提交数 / Commits: $(git rev-list --count HEAD)"
    echo "文件数 / Files: $(git ls-files | wc -l)"
    echo ""
    echo "下一步 / Next steps:"
    echo "1. 访问仓库添加 topics / Visit repo to add topics"
    echo "2. 可选：添加 LICENSE 文件 / Optional: Add LICENSE file"
    echo "3. 可选：添加 GitHub Actions / Optional: Add GitHub Actions"
    echo ""
else
    echo ""
    echo "推送失败 / Push failed，请检查 / Please check:"
    echo "1. GitHub 仓库是否创建成功 / Repository created successfully"
    echo "2. 是否有推送权限 / Have push permission"
    echo "3. 网络连接是否正常 / Network connection is OK"
    echo "4. 认证是否配置正确 / Authentication configured correctly"
fi
