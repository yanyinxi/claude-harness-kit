---
name: commit-push-pr
description: >
  4路CI Gate结构的 git commit + push + PR 创建命令。
  Build、Test、Lint、Security 全部通过才允许提交。
  CRITICAL 安全漏洞阻断即使使用 --no-verify 参数。
  触发词：commit、push、PR、/commit、/pr
user-invocable: true
---

# /commit-push-pr — 4路CI Gate Commit & PR

## CI Gate 结构

所有 Gate 必须通过（AND 逻辑）：

```
┌─────────────────────────────────────┐
│  /commit-push-pr                    │
│                                     │
│  ┌─────────────┐  ✅ Build           │
│  │  Gate 1    │  构建成功，无错误   │
│  └──────┬──────┘                    │
│         │                           │
│  ┌──────▼──────┐  ✅ Test           │
│  │  Gate 2    │  全量测试通过       │
│  └──────┬──────┘                    │
│         │                           │
│  ┌──────▼──────┐  ✅ Lint           │
│  │  Gate 3    │  代码风格检查通过    │
│  └──────┬──────┘                    │
│         │                           │
│  ┌──────▼──────┐  ✅ Security       │
│  │  Gate 4    │  无 CRITICAL 漏洞   │
│  └─────────────┘                    │
│                                     │
│  ✅ ALL GATES PASSED                │
│  → git commit + push + PR           │
└─────────────────────────────────────┘
```

## Gate 详解

### Gate 1：Build（构建）

```bash
# 检测构建命令
if [[ -f package.json ]]; then npm run build
elif [[ -f Makefile ]]; then make build
elif [[ -f pom.xml ]]; then mvn compile
elif [[ -f go.mod ]]; then go build ./...
fi
```

**通过条件**：退出码 = 0

**失败处理**：显示构建错误，阻断

### Gate 2：Test（测试）

```bash
# 运行全量测试
if [[ -f package.json ]]; then npm test -- --coverage
elif [[ -f pom.xml ]]; then mvn test
elif [[ -f pytest.ini ]] || [[ -f pyproject.toml ]]; then pytest -v
fi
```

**通过条件**：所有测试通过，退出码 = 0

**失败处理**：显示失败测试详情，阻断

### Gate 3：Lint（代码风格）

```bash
# 检测并运行 lint
if [[ -f .eslintrc* ]]; then npx eslint src/ --max-warnings 0
elif [[ -f .golangci.yml ]]; then golangci-lint run
elif [[ -f pyproject.toml ]]; then ruff check src/ || true
fi
```

**通过条件**：无 lint 错误（warnings 取决于配置）

**失败处理**：显示 lint 错误，阻断

### Gate 4：Security（安全扫描）

```bash
# 扫描 CWE Top 25 漏洞模式
# 重点：硬编码密钥、SQL注入、XSS、命令注入

# 扫描敏感文件
grep -rn "password\s*=\s*['\"][^'\"]{8,}" src/ --include="*.java" --include="*.py" || true
grep -rn "secret.*=.*['\"][a-zA-Z0-9]{20,}" src/ || true
grep -rn "\.execute\s*\(\s*['\"]SELECT.*\+" src/ || true

# 依赖漏洞扫描
if [[ -f package.json ]]; then npm audit --audit-level=high
elif [[ -f pom.xml ]]; then
  mvn org.owasp:dependency-check-maven:check || true
fi
```

**通过条件**：无 CRITICAL 漏洞

**阻断规则**：CRITICAL 漏洞**即使使用 `--no-verify` 也阻断**

## 安全扫描规则（CWE Top 25）

| CWE | 漏洞类型 | 严重程度 |
|-----|---------|---------|
| CWE-78 | OS Command Injection | CRITICAL |
| CWE-89 | SQL Injection | CRITICAL |
| CWE-798 | Hardcoded Credentials | CRITICAL |
| CWE-79 | XSS (Cross-Site Scripting) | HIGH |
| CWE-502 | Deserialization | HIGH |
| CWE-77 | Command Injection | CRITICAL |
| CWE-306 | Missing Authentication | CRITICAL |

## 命令参数

```
/commit-push-pr                        # 交互式（推荐）
/commit-push-pr --message "fix: ..."   # 直接提交
/commit-push-pr --no-verify           # ⚠️ 仍执行 CI Gate，仅跳过 git hooks
/commit-push-pr --dry-run             # 仅检查，不提交
/commit-push-pr --skip-tests           # ⚠️ 跳过测试 Gate（谨慎使用）
```

## 输出格式

```
🔍 Running CI Gates...

Gate 1: Build .......................... ✅ PASS (2.3s)
Gate 2: Test .......................... ✅ PASS (45 tests, 8.1s)
Gate 3: Lint .......................... ✅ PASS (0 warnings)
Gate 4: Security ....................... ✅ PASS (0 criticals)

✅ ALL GATES PASSED

📝 Commit: feat: add user authentication
🌿 Branch: feature/user-auth
🔗 Remote: origin
🚀 Pushing to origin/feature/user-auth ...
   ✅ Pushed

🔗 PR: https://github.com/owner/repo/pull/123
   Title: feat: add user authentication
   Base: main <- feature/user-auth
```

## 失败输出

```
🔍 Running CI Gates...

Gate 1: Build .......................... ✅ PASS (1.8s)
Gate 2: Test .......................... ❌ FAIL
   ✗ test_user_auth.py::test_invalid_password [500ms]
   ✗ test_user_auth.py::test_missing_token [320ms]
Gate 3: Lint .......................... ✅ PASS
Gate 4: Security ....................... ✅ PASS

❌ CI GATE FAILED — commit blocked

Fix failures before committing:
  1. Run: npm test
  2. Fix the 2 failing tests above
  3. Run /commit-push-pr again
```

## CRITICAL 安全漏洞阻断示例

```
🔍 Running CI Gates...

Gate 1: Build .......................... ✅ PASS
Gate 2: Test .......................... ✅ PASS
Gate 3: Lint .......................... ✅ PASS
Gate 4: Security ....................... 🔴 CRITICAL BLOCKED

   ⚠️ CWE-798: Hardcoded credentials found
   ⚠️ File: src/utils/auth.js:42
   ⚠️ Pattern: apiKey = "sk-antapi03-xxx..."

   🔴 CRITICAL vulnerabilities BLOCK commit
   🔴 (--no-verify does NOT bypass security gates)

Fix: Replace hardcoded secrets with environment variables
```

## 与 git hooks 的关系

- **git commit --no-verify** 跳过 `commit-msg` 和 `pre-commit` hooks
- **CI Gate 不受影响**：Build/Test/Lint/Security 仍强制执行
- 这是**设计意图**：安全 gate 不可绕过

## Red Flags

- 使用 `--no-verify` 绕过安全扫描
- Gate 失败但仍然 push
- 忽略 CRITICAL 安全警告
- 跳过测试 Gate 在非紧急情况下