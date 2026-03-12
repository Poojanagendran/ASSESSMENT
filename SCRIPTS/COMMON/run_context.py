"""
Run context: optional overrides for shared objects so scripts can isolate state
and run in parallel or tests without relying on import order or global singletons.

Usage:
- Default: do nothing. get_*() return the usual module-level singletons.
- Isolation (e.g. parallel run or test): at the start of the script/worker,
  call set_write_excel(Excel()), set_env(Environment()), etc. Then use
  get_write_excel() / get_env() (or keep using the global names that now
  delegate to context). At the end, optionally clear_run_context().

Example for parallel or per-run isolation:
    from SCRIPTS.COMMON.run_context import set_write_excel, clear_run_context
    from SCRIPTS.COMMON.write_excel_new import Excel, get_write_excel
    set_write_excel(Excel())   # this run uses its own Excel
    try:
        # ... script body; get_write_excel() or write_excel_object both use the instance
        pass
    finally:
        clear_run_context()
"""

import contextvars

# Sentinel: context vars use this as default so we can distinguish "unset" from "set to None"
_UNSET = object()
# Context vars: when set to a value, get_*() return it; when _UNSET, get_*() return default from respective module.
_env_ctx: contextvars.ContextVar = contextvars.ContextVar("run_context.env", default=_UNSET)
_write_excel_ctx: contextvars.ContextVar = contextvars.ContextVar("run_context.write_excel", default=_UNSET)
_crpo_common_ctx: contextvars.ContextVar = contextvars.ContextVar("run_context.crpo_common", default=_UNSET)
_assess_ui_common_ctx: contextvars.ContextVar = contextvars.ContextVar("run_context.assess_ui_common", default=_UNSET)


def get_env():
    """Return the current env (override if set), else the default env_obj from environment."""
    v = _env_ctx.get()
    if v is not _UNSET:
        return v
    from SCRIPTS.COMMON.environment import env_obj
    return env_obj


def set_env(env):
    """Set the env for this context (e.g. for tests or a different environment)."""
    _env_ctx.set(env)


def get_write_excel_context():
    """Return the current Excel override if set, else _UNSET. Used by write_excel_new.get_write_excel()."""
    v = _write_excel_ctx.get()
    return None if v is _UNSET else v


def set_write_excel(excel):
    """Set the Excel writer for this context (e.g. for parallel run or test)."""
    _write_excel_ctx.set(excel)


def get_crpo_common():
    """Return the current CRPO common (override if set), else the default crpo_common_obj."""
    v = _crpo_common_ctx.get()
    if v is not _UNSET:
        return v
    from SCRIPTS.CRPO_COMMON.crpo_common import crpo_common_obj
    return crpo_common_obj


def set_crpo_common(obj):
    """Set the CRPO common for this context."""
    _crpo_common_ctx.set(obj)


def get_assess_ui_common():
    """Return the current Assessment UI common (override if set), else the default assess_ui_common_obj."""
    v = _assess_ui_common_ctx.get()
    if v is not _UNSET:
        return v
    from SCRIPTS.UI_COMMON.assessment_ui_common_v2 import assess_ui_common_obj
    return assess_ui_common_obj


def set_assess_ui_common(obj):
    """Set the Assessment UI common for this context (v2 or v3 instance)."""
    _assess_ui_common_ctx.set(obj)


def clear_run_context():
    """Clear all overrides so get_*() fall back to default singletons again."""
    for var in (_env_ctx, _write_excel_ctx, _crpo_common_ctx, _assess_ui_common_ctx):
        var.set(_UNSET)


get_env()