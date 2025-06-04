# Changelog


## [1.2.10] - 2025-05-30

### pironman5
- Added Gitee support with `--gitee` flag in `sf_installer` for package source switching
- Introduced new variant: Pironman 5 Max with expanded features
- Adjusted RGB settings: Brightness reduced from 100 to 50, speed from 0 to 50
- Updated service boot order for proper GPIO resource allocation
- Bumped dependencies: `pm_auto` to v1.2.7, `pm_dashboard` to v1.2.7
- Added version tracking and log removal functionality in installer
- Fixed OLED sleep timeout value validation and deprecated features in base classes

### pm_auto
- Resolved RGB reverse issue using `enumerate` for correct LED ordering
- Added debounce logic to OLED display updates via `DebounceRunner`
- Improved vibration switch: Removed `bounce_time` parameter from initialization
- Enhanced byte formatting with `auto_threshold`
- Added comprehensive tests for byte formatting functions

### pm_dashboard
- Validated OLED timeout input to accept only positive integers/floats

**Links**:
- [pironman5 Compare](https://github.com/sunfounder/pironman5/compare/1.2.6...1.2.10)
- [pm_auto Compare](https://github.com/sunfounder/pm_auto/compare/1.2.5...1.2.7)
- [pm_dashboard Compare](https://github.com/sunfounder/pm_dashboard/compare/1.2.6...1.2.7)

## [1.2.6] - 2025-3-25

- Compatible with Max
- Fix RGB LED extends

## [1.2.3] - 2025-2-18

- Fix stop on close

## [1.2.2] - 2025-2-17

- Fix for remote access