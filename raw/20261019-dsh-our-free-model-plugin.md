---
slug: 20261019-dsh-our-free-model-plugin
source_url: "https://github.com/Ebony-Vinyl/dsh-our-free-model"
canonical_id: "github:Ebony-Vinyl/dsh-our-free-model"
fetched_at: "2026-10-19T08:21:37Z"
reader: "raw.githubusercontent.com README (curl) + GitHub search API (connector) for counts"
captured_by: routine:weekly-hot-list
---

```json
{
  "repo": "Ebony-Vinyl/dsh-our-free-model",
  "github": {
    "stars": 26054,
    "forks": 564,
    "created_at": "2026-09-24T16:17:19Z",
    "language": "JavaScript",
    "license": "MIT",
    "as_of": "2026-10-19",
    "snapshot_2026-10-12": 10191
  }
}
```

# Ebony-Vinyl/dsh-our-free-model — README (verbatim (first 300 of 771 lines, per vault-capture step 1))

<div align="center">
  <img src="icon.svg" alt="Our Free Model — DeepSeek Harness 免费模型插件" width="120">

# dsh-our-free-model

**简体中文** | [English](README_EN.md)

  <img alt="许可证" src="https://img.shields.io/badge/license-MIT-263146?style=flat-square">
  <img alt="零依赖" src="https://img.shields.io/badge/dependencies-zero-4b6fff?style=flat-square">
  <img alt="无构建步骤" src="https://img.shields.io/badge/build%20step-none-7da1de?style=flat-square">
  <img alt="适配内核" src="https://img.shields.io/badge/dsh-0.1.5--0.1.7--rc.2-2f6f4f?style=flat-square">
  <img alt="状态" src="https://img.shields.io/badge/status-beta-f0a441?style=flat-square">
  <br>
  <a href="https://trendshift.io/repositories/261203"><img alt="GITHUB TRENDING 第 1 名，日榜仓库" src="docs/images/trendshift-daily-laurel-gold.svg" width="250" height="55"></a>
  <a href="https://trendshift.io/weekly?language=JavaScript"><img alt="Trendshift JavaScript 周榜第 1 名（2026-10-05 至 2026-10-11，更新中）" src="docs/images/trendshift-weekly-2026-10-11-first-gold.svg" width="250" height="55"></a>
  <br>
  <sub>Trendshift JavaScript 周榜第 1 · 2026-10-05 至 2026-10-11 · 更新中，截至 2026-10-11</sub>

</div>

<div align="center">

> 你只需在 dsh 里装上这个插件，无需登录、注册、填 API Key 或任何其它操作，
> 就能用上包括 DeepSeek V4.1 Flash、Kimi K3 在内的前沿模型——完全免费，不限量。
>
> *All you do is install this plugin in dsh: no login, no sign-up, no API key, nothing
> else. The frontier models are just there — DeepSeek V4.1 Flash, Kimi K3 and the rest.
> Free, with no usage cap.*
>
> 模型清单跟随上游刷新，可用性由**你自己这台机器的网络出口**实测得出，
> 思考强度下发的是真实预算而不是提示词，另附一个 OpenAI 兼容的本地转发端口。
>
> 纯插件挂载：不改内核、无构建步骤、零依赖。

</div>

---

## 交流频道

<div align="center">
  <img src="docs/images/qq-group-qr.png" alt="AI 技术交流学习频道二维码" width="300">
  <br>
  <b>QQ 频道：pd90484671（ai技术交流学习）</b>
  <br>
  扫码加入频道，一起交流插件使用心得、反馈问题与分享玩法。
</div>

---

## 亮点

- **开箱即用，无配置环节**——不需要账号、不需要 Key、不需要在后台申请配额。
- **上游来源公开透明**——免费车道来源为 [OpenCode 的 Zen 网关](https://opencode.ai)，Kilo 渠道来源为 [Kilo AI 的公共网关](https://kilo.ai)，均直连、不经任何第三方中转。请求由谁处理、数据发往何处，见「上游是哪些源」与「免责声明」。
- **清单跟随上游**——模型集合、上下文长度与能力在每次刷新时向上游重新拉取，插件内不保存静态快照。
- **选择器只广播可用的模型**——上游清单已声明但网关明确拒绝路由的模型（返回 `Model is unavailable`、或 404 找不到该 id）从下拉框移除，仅在设置页保留记录并注明拒因；网关自身故障（5xx）、配额限制（429）、超时与断网不属于对模型的判定，一律保持可达；被地区策略拦截的模型归入 region-limited 分组。整轮探测全部被拒时同样保留，选择器不会为空。
- **公告中心 + 实时推送**——仓库维护者在仓库中编辑 JSON 并推送后，所有已安装实例最迟在一个轮询周期内收到；正文为白名单约束下的 HTML，支持图文排版；`urgent` 级别触发全屏弹窗；可选系统级通知。
- **应用内升级**——设置页一键升级：下载 → SHA-256 校验 → 备份 → 原子替换 → 校验回读 → 热重载，任一步失败自动回滚至上一版本。
- **热重载**——升级与代码变更即时生效，无需重启应用；也可在设置页手动触发，或启用文件监视自动重载。
- **按响应体形状判定流式响应**——网关在高负载下会以 `application/json` 的 content-type 返回完整的 SSE 帧序列。插件按响应体形状判定，并将已嗅探的字节重新注入流，既不会导致整轮失败，也不会因 header 与实际内容不符而将可用模型判为不可用。
- **思考强度实际生效**——两类模型两种控制：声明了思考档位的模型（如 DeepSeek V4.1 Flash、GLM 5.3 Flash）给出它自己的档位菜单（Off / Low / High / Max 等），选中值按原值下发到上游 `reasoning_effort`，上游会校验该字段、集合外的取值直接 400；没有档位菜单的模型（MiMo V2.6 等）走预算阶梯——Light / Balanced / Deep 对应输出 token 预算 2 048 / 8 192 / 模型上限，思考不可关闭的模型三档整体翻倍为 4 096 / 16 384 / 模型上限，因为思考与正文共享同一输出额度。两者都逐次调用留痕，设置页每张模型卡均标注档位或该档实际下发的上限（详见「思考强度：档位菜单与预算阶梯」）。
- **不依赖浏览器界面**——插件仅将 llm 作为硬依赖，在没有 web server 的 composition（如 dsh-tui）中同样完成启动并输出模型；看板模块挂载在独立的 fiber 上，待 webServer 就绪后再注册路由，因此既不会阻塞模型车道，也不会因插件先于 web 服务加载而永久丢失设置页。
- **用量看板，数据全部留在本机**——Token 热力图、总量曲线（支持总计与单模型视图）、输出速度与首字延迟逐次采样。不上传任何数据。
- **OpenAI 兼容转发端口**——本机其它工具通过 base URL 与 Key 即可调用这些模型。
- **EAC 渠道（桌面端专属）**——在 DeepSeek Harness 桌面端与 DSHEAC AIO 桌面端中自动解锁一条协付通道，模型以 EAC 前缀显示（如 EAC DeepSeek V4.1 Flash）；凭据加密密封，由宿主指纹闸门把守；该渠道在服务器侧校验 GitHub 授权（登录并 star 本仓库）后才放行对话；在命令行及其它宿主中该通道完全不存在。详见「EAC 渠道」。
- **Kilo 渠道（免密免费池）**——内置 Kilo AI 公共网关的免费模型池（`isFree` 清单实时拉取，含 `kilo-auto/free` 自动路由），无需任何账号或 Key；模型卡带 Kilo 徽章。思考强度与 EAC 渠道同款：模型自身的档位菜单（Off / Low / Medium / High，默认 High），经网关统一的 `reasoning` 参数真实下发——Off 已逐家族实测将思考归零（nemotron、ling、dots、poolside、apodex、cohere）；stepfun 与 liquid 端点强制思考（对关闭请求返回 400）、两个自动路由不透传关闭，这些模型的菜单不含 Off 档。该池由上游免费提供，上游会在其模型卡中声明 prompt 可能被记录用于改进服务——请勿发送敏感内容，详见「免责声明」。
- **聚合渠道，自带 Key**——设置页新增一页，把第三方端点接进同一条模型清单：注册表内置 75 家提供商（NVIDIA NIM、OpenRouter、Groq、Cerebras、SambaNova、Gemini、DeepSeek、Mistral、Together、Fireworks、SiliconFlow、Nebius、Chutes、Hugging Face、Cloudflare、Z.ai、Kimi、MiniMax、QwenCloud/Alibaba、Bedrock、Vertex、Vercel AI Gateway、Azure OpenAI，以及无需账号的 Ollama、LM Studio、llama.cpp），写入 Key（本机免账号的提供商不需要）后其模型即以 `provider/model` 出现在选择器里，也可经本地网关调用。Key 只写入本机 0600 的 settings.json，API 只回显 `hasKey` 与 `…abcd` 指纹；每家可单独启停、测试（列表探测，不花一次生成）、发现模型、覆盖 Base URL 与模型清单。OAuth 与 ADC 认证的提供商照常列出，但标注为不可驱动。
- **省 Token**——三件事：工具输出压缩（RTK）在请求发出前就地重写 `tool_result`（git diff / status / log、grep、find、ls、tree、构建日志、编号转储、搜索清单、重复日志行），实测 40 KB 的 `git diff` 移除 90% 的字节且模型仍能就它作答；提示词瘦身有 caveman 与 ponytail 两族、默认全关；另有五个不占用上游请求的本地应答。设置页用与用量图表同一批统计行显示压缩前后字节、节省比例、压缩块数与统计调用数。
- **路由（降级链）**——把任意车道的模型串成一条命名链，以 `combo:<name>` 作为虚拟模型出现在选择器与网关上；`fallback` 固定从链首开始，`round-robin` 轮换起点并连续 N 轮粘滞。链接在输出任何正文之前失败会被整段丢弃，切换对调用方不可见；思考增量不算正文，因此「想了很久才撞上配额墙」正是降级最有价值的场景。
- **本地网关原生说 Anthropic**——新增 `POST /v1/messages`（流式与非流式，含 thinking / tool_use 块、真实 stop_reason 与流内 error 事件）与 `POST /v1/messages/count_tokens`（本地估算）；`/v1/models` 广播全部车道，含聚合行与链路。网关页新增「接入客户端」分区，按实际绑定的端口与真实要求的密钥生成 Claude Code、Codex、OpenAI SDK、Anthropic SDK、curl 与局域网的可复制配方。
- **接口具备鉴权围栏**——插件 HTTP 路由优先级高于内核 `/api`，因此内置与内核一致的信任检查（优先复用 composition 的 connection 服务，缺失时退回结构化围栏）。
- **十三个白嫖渠道，一体接入**——CodeArts（华为云）、CodeBuddy / WorkBuddy（腾讯）、LobsterAI（有道）、Qoder / Qoder 中国版（阿里系）、TRAE（字节）、Cline、Loomy（讯飞）、Raccoon（商汤）、MiniMax Code、ZCode（智谱）、Gemini（Google Code Assist）十一个账号渠道开箱即用，外加 Kilo 免费车道与原匿名免费通道；OpenCode 账号渠道在本插件中默认停用。各渠道的登录流程、账号池、每日积分领取、模型黑名单与其本地 OpenAI 网关（Chat Completions + Responses，默认 `127.0.0.1:8326`）原样挂载与运行；凭据只写入宿主凭据库，浏览器永远拿不到明文。
- **十一页毛玻璃界面**——设置页顶部导航扩为十一个页面：原有六页（**免费模型**（鱼缸水位 = 可用模型占比）、**EAC 模型**（鱼缸水位 = 协付池压力）、**白嫖模型接入**（十三张渠道卡：登录、账号、模型开关、一键领取积分）、**数据看板**（今日/全部 Token 消耗、平均生成速度、缓存命中率、成功率，账号透视与模型性能表、最近请求总览）、**运行日志**（逐请求明细：结果、耗时、首字、速度、Token 细分，失败原因悬停可见）与**网关设置**（网关开关/端点/密钥；局域网转发中继：监听地址、端口与独立中继密钥）），新增**聚合渠道**（提供商注册表、Key、测试、发现模型、Base URL 与模型清单覆盖）、**省 Token**（压缩开关、两族提示词档位、五个本地应答与节省统计）、**路由**（降级链编辑器）、**插件升级**（版本检查、一键升级与热重载）与**推荐项目**（EAC-Desktop / EAC-Pack / EAC-design-world 三张卡片：简介、直达链接与 Star 按钮，Star / Fork / 最近提交数实时取自 GitHub，取不到就整块不显示）五页；网关设置页另增「接入客户端」分区。页面切换与卡片入场为 150–250 ms 短动效，`prefers-reduced-motion` 下整体关闭。每页都有直达 GitHub 仓库的 Star 按钮。
- **局域网转发中继**——渠道网关本身只监听本机（上游的安全选择）；本插件提供自己的转发门：调用方用插件签发与轮换的中继密钥，转发跳由宿主换用网关凭据（凭据不出宿主进程），仅放行 `/v1/*` 模型接口并带环路保护。

## 你会看到什么

**输入框的模型选择器**

| 分组 | 内容 |
| --- | --- |
| Our Free Model | 当前网络出口可直接使用的模型 |
| Our Free Model · region-limited | 上游对该地区不放行的模型，保留可见但单独隔离 |

被判定为「已声明但不路由」的模型不出现在任何分组中——它们仅在设置页的「不在选择器中」分组保留记录，
附带拒因与探测时间；后续探测重新通过后自动回到选择器。

**设置页** 设置 → Our Free Model，包含七个分区：

- **模型清单**——各模型的可用性、是否支持视觉、上下文窗口、最长输出、各思考档位实际下发的输出上限、实测首字延迟，以及单次调用基准测试按钮。
- **EAC 渠道授权**——一键发起 GitHub 登录（自动打开浏览器，无需复制粘贴）、显示登录名与 star 校验状态、重新检查、退出登录；未授权时模型卡带锁标记。免费车道的模型不受影响。
- **公告中心**——仓库维护者推送的公告流：未读计数、紧急徽章、单条/全部标记已读、检查新公告按钮、系统通知开关。公告正文按白名单渲染 HTML。
- **用量看板**——总览计数、17 周 Token 热力图、总量曲线（Token / 请求数切换，总计与单模型切换）、速度迷你图、按模型汇总表。
- **本地转发**——开关、监听地址与端口、复制 base URL、显示 / 复制 / 轮换 API Key，并提供可直接执行的 curl 示例。
- **插件设置**——总开关、是否展示地区受限模型、探测间隔、默认输出上限，以及当前探测到的出口 IP 与国家。
- **插件升级**——当前/最新版本、检查更新、一键升级（含进度与失败原因）、最近一次升级历史、热重载按钮与文件监视开关。
- **首次启动公告**——分 5 页（前言 / 模型清单 / 使用步骤 / 功能介绍 / 公告与升级），确认一次后不再弹出，除非文案版本号被提升。

## 独立本地服务（开发中）

仓库现在提供两个入口：下文安装的是 **DSH 插件**；`packages/standalone` 是
**无需安装 DSH 的独立本地服务**。从完整源码仓库运行：

```powershell
npm run start:standalone
```

独立服务默认使用 `~/.our-free-model` 和端口 `18900`，拥有自己的 API Key，
不读取插件数据。支持匿名/Kilo、EAC 和原有十三个账号渠道，提供
Chat Completions、Responses API，以及独立网页管理（模型、统计、渠道、EAC、设置、API Key）。
启动后打开终端打印的一次性管理链接即可使用；账号在独立页面登录，也可手动导入插件账号备份。
启动、参数与验证见 [独立服务说明](packages/standalone/README.md)。
独立服务的安装制品与 Release 尚未发布。

## 安装

> **⚠️ 不要通过 npm 安装本插件。**
>
> npm 上的 `dsh-our-free-model` 包**不是本仓库发布的**。它由第三方打包，内容与本仓库
> 不一致：`index.js`、`client.js` 被改动，并额外包含本仓库从未有过的
> `src/channel-visibility.js`。装到它得不到本项目审核过的构建，也拿不到本仓库的签名
> 清单校验与应用内升级。
>
> 请只按本文档下方的方式安装：使用本仓库的 Release 发布包，或本地源码目录。
> 其它渠道出现的同名包一律以本仓库为准。

**命令行（纯 dsh web）**

```
dsh plugin --profile web add /绝对路径/dsh-our-free-model
```

安装完成后重启应用一次。`--profile` 填写实际使用的 profile 名称。

**DSHEAC AIO / 桌面端：请先阅读本节**

部分 DSHEAC AIO / 旧版桌面整合包在启动 web 服务之前会执行 profile 闸门，
限制 profile 中的符号链接或目录 junction。若当前宿主包含该检查，可能报错：

```
PROFILE_UPGRADE_REQUIRED: offline dependency migration is not yet available
```

遇到该闸门时，不要使用 `link:` 依赖或 junction；使用应用内插件管理器，
或下方的本地 tarball 安装。不同宿主的限制以自身日志和安装机制为准。

以真实目录手工安装时，使用可信源码打出的本地 tarball：

1. 创建 `<DSH_HOME>/profiles/<profile>/vendor/`，在审核过的本仓库目录运行 `npm pack --ignore-scripts --pack-destination "<DSH_HOME>/profiles/<profile>/vendor"`，或将本仓库正式发布的同版本 tarball 放入该目录。本地打包不执行 npm 发布。
2. 在 profile 的 `package.json` 的 dependencies 中加入 `"dsh-our-free-model": "file:./vendor/dsh-our-free-model-2.5.4.tgz"`。文件名版本跟随仓库 `package.json`，不要改成同名 npm 注册表版本；再通过宿主的安装流程解析依赖。
3. 在 dsh.profile.bundles 末尾追加 `"dsh-our-free-model"`。

包管理器拥有这份安装的字节时，同时将 bundle config 或插件 `settings.json` 的 `distribution` 设为 `managed`，由包管理器统一更新；应用内升级、公告 feed 与热重载会停用，模型功能保留。以后更新时替换可信 tarball 并同步依赖路径，避免包管理器按旧锁文件恢复旧版本。

若手工复制发布文件，必须复制完整包，包括 `adapter/`、`src/`、`locale/` 和 `vendor/channel-pack/` 下的 `pack.js`、WASM、LICENSE、NOTICE；只复制入口脚本会导致渠道加载失败。

不要再向 cordis.patch.yml 添加条目。被 dsh.profile.bundles 引用的包，其自带的
patch 层会自动生效；两处同时注册将报错 duplicate loader entry id: our-free-model。

**整合包（托管安装）**

插件由整合包（EAC 整合包、Mojobox 等）安装时，更新时机与文件字节由安装方控制：
安装时将 bundle config 设为 distribution: 'managed'（或向 settings.json 写入
同一字段），插件的应用内升级、公告 feed 与热重载即全部停用——两个写入方同时操作
同一安装目录只会导致目录损坏；模型 lane 不受影响。相关验收见
scripts/offline-test.mjs；目录就绪记录（manifest 0.15 / 出处 / 许可 / 完整性）
位于 catalog/ 下。

**启动桌面端前的自检**

可直接调用桌面端自身的闸门代码进行自检：

```
node -e "
const g = require('/sidecar/dist/lib/profile-upgrade.js');
const app = '', profile = '/profiles/';
console.log(g.planProfileUpgrade(app, profile));
g.assertProfileStartup(app, profile);
console.log('startup gate: PASS');
"
```

预期输出为 status: 'compatible'、mismatches 为空数组，随后输出 PASS。
若仅需确认 bundle 组合是否正确而不启动界面：

```
DSH_HOME= dsh --profile  --dump-config | grep our-free-model
```

应当只出现一个 id: our-free-model。

**安装失败：ERR_PNPM_VIRTUAL_STORE_DIR_MAX_LENGTH_DIFF**

该问题源于目标 profile 的 pnpm 状态，与插件仓库无关（报错发生在下载插件之前）：profile 中已有的
node_modules 由旧版 pnpm 生成，dsh 更新后内置的 pnpm 版本发生变化，pnpm 拒绝在旧参数上继续安装。
关闭 dsh，删除该 profile 的 node_modules 与 pnpm-lock.yaml 使其重建，然后重新安装：

```
rd /s /q "%DSH_HOME%\profiles\web\node_modules"
del "%DSH_HOME%\profiles\web\pnpm-lock.yaml"
```

同时出现的 Ignoring broken lockfile 警告会随重建一同消失。

**安装失败：`git ls-remote "git+ssh://git@github.com/..."`（插件市场自动安装）**

插件市场（dsh-plugin-hub）对 git 源的自动安装会把 GitHub 地址交给 pnpm 解析，pnpm 再调用本机
git 执行 `git ls-remote`。若本机 git 配置了 `insteadOf` 重写（常见于把 https 改写为 ssh 的
`url."git+ssh://git@github.com/".insteadOf` 规则），或 SSH 密钥未配置，这一步会在下载任何插件
文件之前失败。处理方式二选一：

- 修正本机 git 配置（`git config --global --get-regexp insteadof` 查看重写规则），保证终端里
  `git ls-remote https://github.com/Ebony-Vinyl/dsh-our-free-model.git` 能成功；
- 改用本地安装：从 Releases 下载发布包解压后 `dsh plugin add <解压目录>`，绕开 git 解析。

**安装失败：`profile "desktop" is managed exclusively by the Electron application`**

这是宿主自身的保护，不是插件问题：桌面端（Electron）的 profile 只允许桌面应用自己管理，
命令行 `dsh plugin add` 无法写入。请在桌面端的插件管理器（设置 → 插件）里完成安装或升级；
命令行安装仅适用于纯 web profile（`dsh web`）。

## 桌面安装包（macOS，社区构建）

DSH 插件本体无需构建、解压即用；**桌面安装包**（Our Free Model 桌面壳）官方目前只发布 Windows 版。macOS 版为社区构建：源码改动见 [PR #421](https://github.com/Ebony-Vinyl/dsh-our-free-model/pull/421)，可逐行审计；预打好的 Apple Silicon（arm64）包以社区 Release 的版本和校验值为准，也可以自己从源码构建（macOS 上执行 `npm --prefix packages/desktop run build`，完整流水线见 `.github/workflows/build-macos.yml`）。

下载后建议先核对校验和（SHA256 见 PR / Release）：

```bash
shasum -a 256 ~/Downloads/Our.Free.Model_<version>_aarch64.dmg
```

**安装后提示「已损坏」或打不开？**

社区构建没有 Apple Developer 账号签名与公证，Gatekeeper 会拦截首次启动——这不是文件真的损坏，以下几种方式任选其一：

1. **右键打开**：在访达中按住 Control 点按应用图标，选择「打开」，在弹窗中再次点按「打开」。
2. **清除隔离属性**（终端）：

   ```bash
   xattr -cr /Applications/Our\ Free\ Model.app
   ```

3. **仍提示损坏时，用 sudo 清除隔离属性**（较新 macOS 对未签名应用校验更严）：

   ```bash
   sudo xattr -rd com.apple.quarantine "/Applications/Our Free Model.app"
   ```

4. **在系统设置中放行**：打开「系统设置 → 隐私与安全性」，若出现「仍要打开」按钮，点按确认。

几点说明：

- 当前社区包为 **Apple Silicon（arm64）**；Intel 机型的 Mac 需自行从源码构建。
- 包内自带 Node 运行时与独立服务，安装后即可使用，无需登录、无需 API Key。
- 该包未经 Apple 签名与公证，是否信任请以上方可审计的源码改动与可复现的 CI 构建记录为准。

## 使用说明

**选择模型**：打开输入框的模型选择器，选择 Our Free Model 分组下的任意模型。选择结果按会话持久化。

**调整思考强度**：同一菜单中的 Effort。声明了思考档位的模型给出它自己的档位（如 Off / Low /
High / Max），选中值按原值下发；其余模型给 Light / Balanced / Deep 三档，档位越高思考占用的
输出预算越多，上限为强制下发，因此档位之间存在可测量的差异。思考与可见回答共享同一输出额度，
因此思考不可关闭的模型会将三档整体上移（设置 → Our Free Model 的模型卡上标注了每档的
实际数值，声明档位的模型则标注档位名）。若回答被截断，可切换至更高档，或调高设置中的
单次输出上限。

**供本机其它工具调用**：设置 → Our Free Model → 本地转发，启用后复制 base URL 并生成 Key。支持：

- GET /v1/models
- POST /v1/chat/completions（流式与非流式）
- POST /v1/responses
- POST /v1/messages（流式与非流式，Anthropic Messages）
- POST /v1/messages/count_tokens（本地估算，插件不含 tokenizer）

端口被占用时插件不会静默失效：先在同一端口重试数轮（刚关闭的监听、刚删除的
portproxy 规则通常在数百毫秒内释放），仍被占用则顺延至下一个可用端口，并在设置页标注
"请求的 18899 不可用，实际监听 18900"，落盘的也是该实际端口。Windows 上最常见的占用
来源是一条 netsh interface portproxy 规则（由 IP Helper 服务承载）：其对 0.0.0.0 的
监听会导致回环绑定直接返回 EACCES（区别于 EADDRINUSE）。netsh interface portproxy show all 可列出规则，netsh interface portproxy reset 可清除规则。

转发端点为全流式：除 `data:` 帧外，思考期间的静默由周期性写出的 SSE 注释帧
（以 `:` 开头）填充，客户端的 idle 超时因此不会将"上游仍在推理"误判为"连接已断开"。思考内容按
reasoning、reasoning_content、reasoning_text 三个字段识别——同一段思考若被上游同时
写入两个字段只计一次——reasoning_details 数组同样识别。上游本身不流式输出思考的模型，此处
也不会产生思考帧，详见「已知边界」。

**供同一网络中的其它设备使用**：同一面板下方还提供"局域网访问"。该功能默认关闭；启用后中继绑定一个可路由地址（默认 0.0.0.0），并要求使用独立的局域网 Key——与上述本机 Key 互不通用，因此任一泄露只需轮换对应一侧，本机已配置的工具不受影响。中继将请求原样转发至本机监听，模型清单、流式行为与错误语义与本机完全一致。端口填 0 表示自动分配（本机 18899 常已被占用或被端口代理占用），启用后面板会显示实际端口与局域网地址。**局域网地址按本机网卡实时读取**：面板在开启期间每 15 秒重读一次，切换到别的网络后不必重开面板。同一台机器常同时持有多张网卡上的私网地址——路由器分配的 `192.168.x.y`，以及虚拟交换机（WSL/Hyper-V/Docker）、VPN 或隧道适配器上的地址——面板把物理网卡的地址排在前面并作为可直接复制的那一条，其余地址列在其下；中继绑定的是所有接口，但某个地址能否被同网段的另一台机器拨通，取决于该地址所属的那张网卡。启用期间，任何能够访问该主机的用户均可使用此 Key 消耗本机的免费额度，因此请仅在可信网络中启用，必要时通过防火墙限制来源网段。

**重新核对地区**：点击"重新探测可用性"，将按当前出口重新执行探测。切换 VPN 状态后再执行一次，
地区受限模型会在两个分组之间自动迁移。

**接收公告**：全自动。仓库维护者推送新公告后，运行中的插件在一个轮询周期内（默认
30 分钟，也可在公告中心点击"检查新公告"立即拉取）收到通知：普通公告弹出 toast，
`urgent` 级别直接触发全屏弹窗，两者均会进入公告中心并保留未读标记。如需同时接收
系统级通知，在公告中心点击"开启系统通知"。

**升级插件**：设置 → Our Free Model → 插件升级 → 检查更新 → 立即升级。全流程
在应用内完成（下载 → 校验 → 备份 → 替换 → 热重载），无需重新安装，也无需
重启应用。升级失败会自动回滚至上一版本并给出失败原因。
