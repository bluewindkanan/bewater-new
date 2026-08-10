# BeWater 代码修复计划

**日期**：2026-08-10
**范围**：修复评审报告发现的实现问题
**方法**：TDD，按 P0→P3 顺序执行

---

## P0（半天）：数据一致性

### P0-1: S1 回填 concept 重构到 src

**问题**：`.claude/skills/` 被 `.gitignore` 忽略，src 与部署版漂移，`install.sh` 会回退系统。

**修复步骤**：
1. 对比三处差异：
   ```bash
   diff -r src/skills/bw-ideate .claude/skills/bw-ideate
   diff -r src/skills/bw-shape .claude/skills/bw-shape
   diff -r src/skills/bw-solution-shape .claude/skills/bw-solution-shape
   ```
2. 人工审查差异，确认部署版为正确版本（含 2026-08-09 重构）
3. 将部署版内容回填到 `src/skills/`
4. 提交 `git commit -m "fix(skills): backfill concept lifecycle refactor to src"`

**验证**：
```bash
diff -r src/skills/bw-ideate .claude/skills/bw-ideate  # 应无差异
diff -r src/skills/bw-shape .claude/skills/bw-shape    # 应无差异
```

**工作量**：0.5-1 小时（含人工审查）

---

### P0-2: S3 统一 validation_status 枚举

**问题**：`AssumptionValidationStatus` 有 `testing`，但真实态全是 `untested`，`validate_all` 可能加载真实态崩溃。

**修复步骤**：
1. 决定统一枚举值（建议保留文档的 `untested/testing/supported/falsified/inconclusive`）
2. 在 `src/bw/schema.py` 补充枚举
3. 写 migration 脚本处理存量 `untested` → 保持不变（`untested` 本身有效）
4. 补 CI 门检查枚举一致性

**验证**：
```bash
python -c "
from src.bw.schema import AssumptionValidationStatus
print([s.value for s in AssumptionValidationStatus])
# 应输出: ['untested', 'testing', 'supported', 'falsified', 'inconclusive']
"
```

**工作量**：0.5 小时

---

### P0-3: M7 .gitignore 排除 backup 文件

**问题**：6 个 backup 文件被 git 追踪。

**修复步骤**：
1. 加到 `.gitignore`：
   ```
   _bewater/.backup-*
   _bewater/.bw-lock
   _bewater/.tmp-*
   ```
2. 清已追踪文件：
   ```bash
   git rm --cached _bewater/.backup-*
   git rm --cached _bewater/.bw-lock 2>/dev/null || true
   ```
3. 提交

**验证**：
```bash
git status  # 应无 backup 文件
```

**工作量**：0.25 小时

---

## P1（1-2 天）：门控机械化

### P1-1: S4 L4 硬门控机械化

**问题**：`l4_obligation_open` 定义但未消费，L4+ 承诺落空。

**修复步骤**：
1. 在 `src/bw/gate_scan.py` 新增 `_score_l4_obligations` 函数
2. 对所有 `l4_obligation_open==True` 的 Achilles，返回禁止 Go
3. 加入 `_G1_SCORERS` 和 `_G2_SCORERS`
4. 写 eval 断言测试

**实现**：
```python
def _score_l4_obligations(artifacts, active):
    """L4+ behavioral evidence is a hard gate criterion."""
    open_l4 = [a for a in active if a.is_achilles_heel and a.l4_obligation_open]
    if open_l4:
        ids = ", ".join(a.id for a in open_l4)
        return Criterion(
            "l4-obligations",
            False,
            True,
            f"methodology-deviation: {len(open_l4)} Achilles with open L4 obligations: {ids}",
        )
    return Criterion("l4-obligations", True, False)
```

**验证**：
```bash
# 写 eval 场景：Achilles 有 L4 obligation 但 evidence_level < L4
# 期望 gate 返回禁止 Go
```

**工作量**：2-3 小时

---

### P1-2: S5 F/P/E/T 辅助函数

**问题**：只匹配字面串 `"F/P/E/T"`，合法变体被判失败。

**修复步骤**：
1. 在 `src/bw/` 新增 `_has_fpet_signoff(meta)` 函数
2. 接受三种格式：
   - 字面串 `"F/P/E/T"`
   - 4 条独立 signoff（F/P/E/T 各一条）
   - 结构化 dict（`{"type": "fpet", ...}`）
3. `gate_scan.py` 和 validator 共用

**实现**：
```python
def _has_fpet_signoff(meta: schema.ArtifactMeta) -> bool:
    """Check if artifact has F/P/E/T signoff (flexible)."""
    for signoff in (meta.signoffs or []):
        if not isinstance(signoff, dict):
            continue
        what = signoff.get("what", "")
        if what == "F/P/E/T":
            return True
        # 检查 4 条独立签核
        if what in ("Factual", "Plausible", "Emergent", "Transformative"):
            # 需检查四条都存在...
            pass
    return False
```

**验证**：写 3 个 eval 场景测试三种格式

**工作量**：1-2 小时

---

### P1-3: M4 补 concept skill eval 场景

**问题**：评审报告说 0 场景，但实际已各有 2 个。需验证覆盖度。

**修复步骤**：
1. 审计现有 2 个场景是否覆盖关键路径
2. 补充缺失场景（seed 无 OA、concept recycle 等）

**验证**：全量 eval 通过

**工作量**：1 小时（视场景数）

---

### P1-4: M9 keep_backups=0 修复

**问题**：`keep_backups=0` 反而删除所有备份。

**修复**：
```python
# src/bwkit/cas.py:150
# 旧: for extra in backups[:-keep_backups]:
# 新:
extras = backups if keep_backups == 0 else backups[:-keep_backups]
for extra in extras:
    extra.unlink()
```

**验证**：
```bash
# 测试用例
python3 -m pytest tests/test_cas.py::test_keep_backups_zero
```

**工作量**：0.5 小时

---

## P2：设计/覆盖缺口

### P2-1: M1 scope 诚实声明

**修复**：在 `CLAUDE.md` 显式声明：
```markdown
## Scope
本工具包仅覆盖决策段（Immersion→G2）。
执行段（Design/Build/Launch/Grow）与 G3/G4 未实现，交下游交付系统。
```

**工作量**：0.25 小时

---

### P2-2: M8 TOCTOU 竞争修复

**问题**：`acquire_lock` 读判定 stale→replace 之间有窗口。

**修复**：改用 `fcntl.flock` 或抢占后重读确认：
```python
def acquire_lock(root, owner, ttl_seconds=3600):
    # ... 原有逻辑 ...
    os.replace(tmp, path)  # 抢占后重读
    holder = _read_lock(path)
    if holder.get("owner") != owner:
        raise LockError("lost race after preempt")
```

**工作量**：1 小时

---

### P2-3: N2 多位数 gate 排序

**问题**：`G1 < G10 < G2`，最新 baseline 可能选错。

**修复**：按 gate 数值排序：
```python
# src/bw/ledger_ops.py:297
candidates.sort(key=lambda x: int(x[0].split('-')[1][1:]) if x[0].startswith('G') else 0)
```

**工作量**：0.5 小时

---

### P2-4: M10 acquire_lock 副作用

**问题**：无条件 `mkdir _bewater`。

**修复**：
```python
def acquire_lock(root, owner, ttl_seconds=3600):
    root = Path(root)
    if not (root / "_bewater").exists():
        raise LockError("no _bewater/ directory; run 'bwkit init' first")
    # ...
```

**工作量**：0.25 小时

---

### P2-5: M5 健康焦虑路由软阻断

**问题**：`≥2 健康焦虑` 只显示不强制。

**修复**：在 `bw-ideate` 路由器加软阻断：
```python
healthy_anxieties = sum(1 for c in concepts if c.get("healthy_anxiety"))
if healthy_anxieties < 2:
    # 软阻断：需人显式覆盖
```

**工作量**：1 小时

---

### P2-6: M6 backtrack 角色纠偏

**修复**：在 `CLAUDE.md` 把 backtrack 从 router 移出，单列「恢复能力」。

**工作量**：0.25 小时

---

## P3：次要清理

### P3-1: N1 fence 错误友好化

**修复**：
```python
# src/bw/io.py
try:
    end = text.index("\n---\n", 4)
except ValueError:
    raise ValueError(f"malformed artifact: missing closing fence in {path}")
```

**工作量**：0.25 小时

---

### P3-2: 其他次要清理

- 死字段删除：`Ledger.next_id`、`Assumption.affects`
- stdin JSON 解析错误捕获
- `validate_all` O(N²) 优化（评审报告建议，但实际 trace 已是 O(V+E)，需评估）
- `action-plan.md` 抽到 `_bw-shared/`
- router 选择 UX 一致化

**工作量**：2-3 小时

---

## 执行顺序

```
P0-1 → P0-2 → P0-3 → [提交] →
P1-4 → P1-1 → P1-2 → P1-3 → [提交] →
P2-1 → P2-2 → P2-3 → P2-4 → P2-5 → P2-6 → [提交] →
P3-1 → P3-2
```

**总工作量**：1.5-2 天（P0+P1 关键路径）

---

## 回归门

每个优先级完成后：
```bash
python -m pytest tests/ -x -q
python -m bwkit validate_all
```

全完成后：
```bash
python -m pytest tests/ --cov
scripts/verify.py  # 全 skill eval
```
