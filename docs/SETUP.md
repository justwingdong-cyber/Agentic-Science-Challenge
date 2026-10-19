# 工具配置

本项目初始化时验证版本：Playground CLI 0.1.40、Bohr CLI 2.7.24。版本记录用于复现，不要求所有读者永久固定这些工具版本。

```bash
playground --help
playground auth status
bohr version
bohr auth status --verify
bohr skills list
```

官方推荐安装：

```bash
curl -fsSL https://play.bohrium.com/install.sh | bash
npm install -g @dptech-corp/bohr-cli@latest
```

Windows 可使用 Git Bash 运行脚本，或按 [Bohrium 安装文档](https://bohrium-doc.dp.tech/en/docs/bohrctl/install/) 配置 CLI。

设备登录：

```bash
bohr auth login --device --no-wait --json
# 在浏览器完成 CLI 给出的授权流程，再执行：
bohr auth login --resume
bohr auth status --verify
```

Agent 账号与人类账号分开管理。通过 `PLAYGROUND_CREDENTIALS_PATH` 指向本机私有 Agent 凭据文件，再运行 Playground 命令；不要把凭据文件复制进仓库。

云端计算前读取相关内嵌技能：

```bash
bohr skills read bohr-sandbox
bohr skills read bohr-job
bohr skills read bohr-project
bohr skills read bohr-dataset
```

账户登录成功不等于已获取比赛专项额度；实际创建资源前检查可用项目、资源和计费渠道。初始化阶段无需启动计算资源。
