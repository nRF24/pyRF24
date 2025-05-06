# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
<!-- markdownlint-disable MD024 -->

## [0.5.0] - 2025-05-06

### <!-- 6 --> 📦 Dependency updates

- Bump pypa/cibuildwheel from 2.22.0 to 2.23.0 in the github-actions group by \@dependabot[bot] in [#104](https://github.com/nRF24/pyRF24/pull/104)
- Bump the rf24-submodules group with 3 updates by \@dependabot[bot] in [#110](https://github.com/nRF24/pyRF24/pull/110)

[0.5.0]: https://github.com/nRF24/pyRF24/compare/v0.4.5...v0.5.0

Full commit diff: [`v0.4.5...v0.5.0`][0.5.0]

## [0.4.5] - 2025-02-07

### <!-- 6 --> 📦 Dependency updates

- Bump RF24 from `6f3da43` to `929a5aa` in the rf24-submodules group by \@dependabot[bot] in [#101](https://github.com/nRF24/pyRF24/pull/101)

### <!-- 9 --> 🗨️ Changed

- Bump version to v0.4.5 by \@2bndy5 in [`4160298`](https://github.com/nRF24/pyRF24/commit/41602984c2c599cb74d127a1bd960758c12b2360)

[0.4.5]: https://github.com/nRF24/pyRF24/compare/v0.4.4...v0.4.5

Full commit diff: [`v0.4.4...v0.4.5`][0.4.5]

## [0.4.4] - 2025-01-31

### <!-- 6 --> 📦 Dependency updates

- Bump pypa/gh-action-pypi-publish in the github-actions group by \@dependabot[bot] in [#99](https://github.com/nRF24/pyRF24/pull/99)
- Bump the rf24-submodules group with 2 updates by \@dependabot[bot] in [#100](https://github.com/nRF24/pyRF24/pull/100)

### <!-- 9 --> 🗨️ Changed

- Bump version to v0.4.4 by \@2bndy5 in [`54ea3fb`](https://github.com/nRF24/pyRF24/commit/54ea3fb1bfe09610371d2f08d0d8b92ea4109a8f)

[0.4.4]: https://github.com/nRF24/pyRF24/compare/v0.4.3...v0.4.4

Full commit diff: [`v0.4.3...v0.4.4`][0.4.4]

## [0.4.3] - 2025-01-30

### <!-- 2 --> 🚫 Deprecated

- Update pybind11 submodule to v2.13.6 by \@2bndy5 in [`192d318`](https://github.com/nRF24/pyRF24/commit/192d318792016ae7f7fa4a90fdeaa03eae72d8c6)

### <!-- 4 --> 🛠️ Fixed

- Use tx_standby() in streaming_data.py by \@2bndy5 in [`3f8088c`](https://github.com/nRF24/pyRF24/commit/3f8088cf2cec737b690edcdf4a4d51b3c8ace879)

### <!-- 6 --> 📦 Dependency updates

- Bump the rf24-submodules group across 1 directory with 3 updates by \@dependabot[bot] in [#95](https://github.com/nRF24/pyRF24/pull/95)
- Bump the github-actions group across 1 directory with 2 updates by \@dependabot[bot] in [#93](https://github.com/nRF24/pyRF24/pull/93)

### <!-- 8 --> 📝 Documentation

- Doc builds for PEP594 by \@2bndy5 in [`4644a90`](https://github.com/nRF24/pyRF24/commit/4644a908c4a6250f36fc1bf2a653021048e2d5b5)

### <!-- 9 --> 🗨️ Changed

- Update release CI by \@2bndy5 in [#98](https://github.com/nRF24/pyRF24/pull/98)
- Bump version to v0.4.3 by \@2bndy5 in [`8454321`](https://github.com/nRF24/pyRF24/commit/84543212c413cbaa54f10455864287137c38c6df)

[0.4.3]: https://github.com/nRF24/pyRF24/compare/v0.4.2...v0.4.3

Full commit diff: [`v0.4.2...v0.4.3`][0.4.3]

## [0.4.2] - 2024-10-05

### <!-- 1 --> 🚀 Added

- Add armv7l to CI qemu platforms by \@2bndy5 in [`c434ef1`](https://github.com/nRF24/pyRF24/commit/c434ef1f54c8c6afb940c497e640b6ef8c5b80be)

### <!-- 6 --> 📦 Dependency updates

- Bump pypa/cibuildwheel from 2.19.2 to 2.21.2 in the github-actions group across 1 directory by \@dependabot[bot] in [#83](https://github.com/nRF24/pyRF24/pull/83)
- Bump the rf24-submodules group across 1 directory with 3 updates by \@dependabot[bot] in [#84](https://github.com/nRF24/pyRF24/pull/84)

### <!-- 9 --> 🗨️ Changed

- Enable musl linux release builds or aarch64 and armv7l by \@2bndy5 in [`e117588`](https://github.com/nRF24/pyRF24/commit/e1175888134012fada79f6128894a1b855754e89)
- [CI] setup qemu for all supported platforms by \@2bndy5 in [`e6e7970`](https://github.com/nRF24/pyRF24/commit/e6e79703e75f3a5151ff7274aa9e6e0c68aaef3a)
- Bump version to v0.4.2 by \@2bndy5 in [`7d6bb94`](https://github.com/nRF24/pyRF24/commit/7d6bb94befeecb414ea1692d0990f8f912acdcda)

[0.4.2]: https://github.com/nRF24/pyRF24/compare/v0.4.1...v0.4.2

Full commit diff: [`v0.4.1...v0.4.2`][0.4.2]

## [0.4.1] - 2024-07-05

### <!-- 4 --> 🛠️ Fixed

- Fix ble example about powering down radio by \@2bndy5 in [`f59f8b2`](https://github.com/nRF24/pyRF24/commit/f59f8b20a7a968f5393cdab41869a393d47da3ee)

### <!-- 6 --> 📦 Dependency updates

- Bump pypa/cibuildwheel from 2.17.0 to 2.19.2 in the github-actions group by \@dependabot[bot] in [#74](https://github.com/nRF24/pyRF24/pull/74)
- Bump the rf24-submodules group across 1 directory with 3 updates by \@dependabot[bot] in [#75](https://github.com/nRF24/pyRF24/pull/75)

### <!-- 8 --> 📝 Documentation

- Update dependabot config by \@2bndy5 in [#70](https://github.com/nRF24/pyRF24/pull/70)

### <!-- 9 --> 🗨️ Changed

- Adjust description in package metadata by \@2bndy5 in [`4bd8a43`](https://github.com/nRF24/pyRF24/commit/4bd8a4392c87e17d4a1179aa9e12b34bd204f04b)
- Update examples' comment about pin numbers by \@2bndy5 in [`8a2bc41`](https://github.com/nRF24/pyRF24/commit/8a2bc41633c8ec272e62714973fd44135c48dfe7)
- Update dependabot.yml by \@2bndy5 in [`663939e`](https://github.com/nRF24/pyRF24/commit/663939ea894612c9bdfe624e2a95940ad0aee8d4)

[0.4.1]: https://github.com/nRF24/pyRF24/compare/v0.4.0...v0.4.1

Full commit diff: [`v0.4.0...v0.4.1`][0.4.1]

## [0.4.0] - 2024-06-16

### <!-- 4 --> 🛠️ Fixed

- Unify all compiled C++ into 1 binary file by \@2bndy5 in [#64](https://github.com/nRF24/pyRF24/pull/64)

### <!-- 6 --> 📦 Dependency updates

- Bump RF24Network from `ba5a2a5` to `219d055` by \@dependabot[bot] in [#65](https://github.com/nRF24/pyRF24/pull/65)
- Bump RF24 from `c200b7c` to `0aac3d5` by \@dependabot[bot] in [#66](https://github.com/nRF24/pyRF24/pull/66)
- Bump RF24Mesh from `7c30deb` to `8f030b4` by \@dependabot[bot] in [#67](https://github.com/nRF24/pyRF24/pull/67)

[0.4.0]: https://github.com/nRF24/pyRF24/compare/v0.3.0...v0.4.0

Full commit diff: [`v0.3.0...v0.4.0`][0.4.0]

## [0.3.0] - 2024-04-09

### <!-- 1 --> 🚀 Added

- Expose RF24_DRIVER and fix linking to shared utility driver libs by \@2bndy5 in [#46](https://github.com/nRF24/pyRF24/pull/46)

### <!-- 6 --> 📦 Dependency updates

- Bump actions/setup-python from 4 to 5 by \@dependabot[bot] in [#29](https://github.com/nRF24/pyRF24/pull/29)
- Bump actions/upload-artifact from 3 to 4 by \@dependabot[bot] in [#30](https://github.com/nRF24/pyRF24/pull/30)
- Bump pypa/cibuildwheel from 2.16.2 to 2.16.4 by \@dependabot[bot] in [#31](https://github.com/nRF24/pyRF24/pull/31)
- Bump pypa/cibuildwheel from 2.16.4 to 2.16.5 by \@dependabot[bot] in [#32](https://github.com/nRF24/pyRF24/pull/32)
- Bump RF24 from `638095e` to `9eca153` by \@dependabot[bot] in [#39](https://github.com/nRF24/pyRF24/pull/39)
- Bump pypa/cibuildwheel from 2.16.5 to 2.17.0 by \@dependabot[bot] in [#44](https://github.com/nRF24/pyRF24/pull/44)
- Bump RF24Network from `4e804ee` to `48c8fd6` by \@dependabot[bot] in [#43](https://github.com/nRF24/pyRF24/pull/43)
- Bump RF24Mesh from `38ee022` to `087af89` by \@dependabot[bot] in [#42](https://github.com/nRF24/pyRF24/pull/42)
- Supplement SPIDEV & RPi drivers with copy of linux/gpio.h by \@2bndy5 in [#49](https://github.com/nRF24/pyRF24/pull/49)
- Bump RF24 from `a6eae52` to `7441eef` by \@dependabot[bot] in [#51](https://github.com/nRF24/pyRF24/pull/51)
- Bump RF24 from `7441eef` to `5d645ae` by \@dependabot[bot] in [#53](https://github.com/nRF24/pyRF24/pull/53)
- Bump RF24Mesh from `087af89` to `7c30deb` by \@dependabot[bot] in [#56](https://github.com/nRF24/pyRF24/pull/56)
- Bump RF24Network from `48c8fd6` to `ba5a2a5` by \@dependabot[bot] in [#54](https://github.com/nRF24/pyRF24/pull/54)
- Bump RF24 from `5d645ae` to `c200b7c` by \@dependabot[bot] in [#55](https://github.com/nRF24/pyRF24/pull/55)
- Bump peaceiris/actions-gh-pages from 3 to 4 in the actions group by \@dependabot[bot] in [#57](https://github.com/nRF24/pyRF24/pull/57)

### <!-- 8 --> 📝 Documentation

- Update clang format by \@2bndy5 in [#35](https://github.com/nRF24/pyRF24/pull/35)

### <!-- 9 --> 🗨️ Changed

- Update scanner by \@2bndy5 in [#47](https://github.com/nRF24/pyRF24/pull/47)
- Inline badges in README by \@2bndy5 in [`66d85c1`](https://github.com/nRF24/pyRF24/commit/66d85c1022e6cc1f80f030cbdbd1e53b675162e3)
- Update pypi downloads badge in README by \@2bndy5 in [`60f2672`](https://github.com/nRF24/pyRF24/commit/60f2672a5df2ff04810e6ebde560ae94c233323e)

[0.3.0]: https://github.com/nRF24/pyRF24/compare/v0.2.5...v0.3.0

Full commit diff: [`v0.2.5...v0.3.0`][0.3.0]

## [0.2.5] - 2023-12-05

### <!-- 4 --> 🛠️ Fixed

- Fix typo in README by \@michael-sulyak in [#25](https://github.com/nRF24/pyRF24/pull/25)

### <!-- 6 --> 📦 Dependency updates

- Bump pypa/cibuildwheel from 2.16.1 to 2.16.2 by \@dependabot[bot] in [#26](https://github.com/nRF24/pyRF24/pull/26)
- Bump RF24Network from `a334fa6` to `4e804ee` by \@dependabot[bot] in [#27](https://github.com/nRF24/pyRF24/pull/27)

### <!-- 9 --> 🗨️ Changed

- [RF24 wrapper] use `rf24_gpio_pin_t` and `RF24_PIN_INVALID` by \@2bndy5 in [#28](https://github.com/nRF24/pyRF24/pull/28)

[0.2.5]: https://github.com/nRF24/pyRF24/compare/v0.2.4...v0.2.5

Full commit diff: [`v0.2.4...v0.2.5`][0.2.5]

## New Contributors
* \@michael-sulyak made their first contribution in [#25](https://github.com/nRF24/pyRF24/pull/25)
## [0.2.4] - 2023-09-27

### <!-- 6 --> 📦 Dependency updates

- Bump actions/checkout from 3 to 4 by \@dependabot[bot] in [#19](https://github.com/nRF24/pyRF24/pull/19)
- Bump docker/setup-qemu-action from 2 to 3 by \@dependabot[bot] in [#23](https://github.com/nRF24/pyRF24/pull/23)
- Bump pypa/cibuildwheel from 2.12.0 to 2.16.1 by \@dependabot[bot] in [#21](https://github.com/nRF24/pyRF24/pull/21)
- Bump RF24 from `a028813` to `638095e` by \@dependabot[bot] in [#24](https://github.com/nRF24/pyRF24/pull/24)

### <!-- 9 --> 🗨️ Changed

- Use dependabot by \@2bndy5 in [#18](https://github.com/nRF24/pyRF24/pull/18)

[0.2.4]: https://github.com/nRF24/pyRF24/compare/v0.2.3...v0.2.4

Full commit diff: [`v0.2.3...v0.2.4`][0.2.4]

## New Contributors
* \@dependabot[bot] made their first contribution in [#24](https://github.com/nRF24/pyRF24/pull/24)
## [0.2.3] - 2023-07-28

### <!-- 4 --> 🛠️ Fixed

- Fix typo in topology doc by \@2bndy5 in [`17fce18`](https://github.com/nRF24/pyRF24/commit/17fce185360beaf1ba56ca31cc7148f870f7591a)

### <!-- 8 --> 📝 Documentation

- Update submodules and docs by \@2bndy5 in [#17](https://github.com/nRF24/pyRF24/pull/17)

[0.2.3]: https://github.com/nRF24/pyRF24/compare/v0.2.2...v0.2.3

Full commit diff: [`v0.2.2...v0.2.3`][0.2.3]

## [0.2.2] - 2023-01-19

### <!-- 8 --> 📝 Documentation

- Small updates by \@2bndy5 in [#14](https://github.com/nRF24/pyRF24/pull/14)

### <!-- 9 --> 🗨️ Changed

- Replace relative URLs in README with absolute URLs by \@2bndy5 in [`c631a06`](https://github.com/nRF24/pyRF24/commit/c631a06bcab736c11840c5b9b634a73e29b1799d)

[0.2.2]: https://github.com/nRF24/pyRF24/compare/v0.2.1...v0.2.2

Full commit diff: [`v0.2.1...v0.2.2`][0.2.2]

## [0.2.1] - 2022-08-26

### <!-- 2 --> 🚫 Deprecated

- Expose old open pipe funcs by \@2bndy5 in [#12](https://github.com/nRF24/pyRF24/pull/12)

[0.2.1]: https://github.com/nRF24/pyRF24/compare/v0.2.0...v0.2.1

Full commit diff: [`v0.2.0...v0.2.1`][0.2.1]

## [0.2.0] - 2022-07-23

### <!-- 1 --> 🚀 Added

- Add RF24, RF24Network, RF24Mesh as submodules & copied wrappers to pkg folder by \@2bndy5 in [`4742dcd`](https://github.com/nRF24/pyRF24/commit/4742dcdf4d7b8a35ca2f6a2de0ecde24d257e1e2)
- Add toml; mv submods, wraps, & pkg to src dir by \@2bndy5 in [`366ffb5`](https://github.com/nRF24/pyRF24/commit/366ffb50a97fc3b20caf638e2bbad508263ffb9d)
- Add pybind11 submodule by \@2bndy5 in [`82cb073`](https://github.com/nRF24/pyRF24/commit/82cb073bd57c8f3509d635265ad46c1b9413115d)
- Add scanner example & some more constants by \@2bndy5 in [`e0ecac5`](https://github.com/nRF24/pyRF24/commit/e0ecac5322885735c119f916ecf9e419fa539a89)
- Add mesh tx example and fix net rx example by \@2bndy5 in [`9fa4220`](https://github.com/nRF24/pyRF24/commit/9fa4220170c8511e4c1b0c804ffc84b10dfb0d17)
- Add ble example by \@2bndy5 in [`6c04c06`](https://github.com/nRF24/pyRF24/commit/6c04c06571d127931326e6c6694ab5d0498ae118)
- Add LF to printf debugging calls by \@2bndy5 in [`9a3af91`](https://github.com/nRF24/pyRF24/commit/9a3af91c3faff7e3572c3129cd6f3cfe96ae2dd8)
- Add docstr to address_repr() by \@2bndy5 in [`a5659b9`](https://github.com/nRF24/pyRF24/commit/a5659b971231d7edda612e506f5c18727234c1c1)
- AddrList docs; force addrListStruct as read-only by \@2bndy5 in [`05ac448`](https://github.com/nRF24/pyRF24/commit/05ac4486a997ffc98467049de3271e6907a18840)
- Add gitattributes to normalize line endings by \@2bndy5 in [`87e8151`](https://github.com/nRF24/pyRF24/commit/87e815157eab9fe3559e29751b685d4af711e9e2)
- Add old cpp-like py wrapper API by \@2bndy5 in [`ff8b6f2`](https://github.com/nRF24/pyRF24/commit/ff8b6f21a5a94d947d9c2d4440deffae78ac618c)
- Add payloadSize attr from old Rf24 wrapper by \@2bndy5 in [`ee6da46`](https://github.com/nRF24/pyRF24/commit/ee6da4681941f8ec2231591f21c87e0bcfe43a5f)
- Added more from old network and mesh wrappers by \@2bndy5 in [`17279db`](https://github.com/nRF24/pyRF24/commit/17279dbe08b36af12afd4795e0e048e78f897bdc)
- AddrListStruct has read-only properties by \@2bndy5 in [`324b6d8`](https://github.com/nRF24/pyRF24/commit/324b6d87b8808adb59310ffd3596d510efd61ef7)
- Merge pull request \#9 from nRF24/add-camel-case by \@TMRh20 in [#9](https://github.com/nRF24/pyRF24/pull/9)

### <!-- 3 --> 🗑️ Removed

- Update submodules & prepare for pypi distribution by \@2bndy5 in [#11](https://github.com/nRF24/pyRF24/pull/11)

### <!-- 4 --> 🛠️ Fixed

- Fix last step in CI workflow by \@2bndy5 in [`4fd6401`](https://github.com/nRF24/pyRF24/commit/4fd640184dc9a6350f2c54e0249e7eb98e8cc883)
- Fix typo by \@2bndy5 in [`07318be`](https://github.com/nRF24/pyRF24/commit/07318be51b6848103347eecd8791cbfcfac6b1c9)
- Fix a typo and adjust pyRF24 examples by \@2bndy5 in [`302f929`](https://github.com/nRF24/pyRF24/commit/302f929afc06094848982af9fd55fd1ebdd27523)
- Fix scanner example by \@2bndy5 in [`20a6ed1`](https://github.com/nRF24/pyRF24/commit/20a6ed106d56e9f48210ea9688e4d345058e7f62)
- Fix net_tx example by \@2bndy5 in [`2de68f1`](https://github.com/nRF24/pyRF24/commit/2de68f16f521e9b3563878f329d0629d92fcc69b)
- Fix super() calls in FakeBLE by \@2bndy5 in [`f1c11ad`](https://github.com/nRF24/pyRF24/commit/f1c11ad9229a9634062f3e2f6e6c321a2c2c1d14)
- Fix missed a super() call by \@2bndy5 in [`2c3fa24`](https://github.com/nRF24/pyRF24/commit/2c3fa245afad9fba37daa90c7cd973851e8a908b)
- Fix BLE advertised PA level by \@2bndy5 in [#8](https://github.com/nRF24/pyRF24/pull/8)

### <!-- 8 --> 📝 Documentation

- Complete docs; ready for HW test by \@2bndy5 in [`283d6da`](https://github.com/nRF24/pyRF24/commit/283d6da6d9ba0c019ec95ac2d39bacfd613ef32d)
- __init__ docs look ugly, but it shows up by \@2bndy5 in [`0926341`](https://github.com/nRF24/pyRF24/commit/09263418cc22d62235e161b504ff99b8ae1a89e5)
- Upload bleeding edge docs to gh-pages branch by \@2bndy5 in [`566bd0e`](https://github.com/nRF24/pyRF24/commit/566bd0ea7e482c8ced178936d1c332921361cb6c)
- Specify language for newer docs theme by \@2bndy5 in [`861b1b1`](https://github.com/nRF24/pyRF24/commit/861b1b1814159d5f6c753949e4dee64103d8be87)
- Docs proofread by \@2bndy5 in [`968d104`](https://github.com/nRF24/pyRF24/commit/968d104789ee4947667da606a10803010fca60a9)
- Filling out the docs by \@2bndy5 in [`0a07a6c`](https://github.com/nRF24/pyRF24/commit/0a07a6c47a93800f4e39af7081cf70a61532dd8a)
- Embed docs within fake_ble module by \@2bndy5 in [`6402927`](https://github.com/nRF24/pyRF24/commit/640292790df6f064225f65c4e1368228990a9899)
- Doc updates and upload CI artifacts by \@2bndy5 in [`35e16f5`](https://github.com/nRF24/pyRF24/commit/35e16f546381180cbea0ef764865a2b5f324bbf6)
- Only update docs if CI run on upstream by \@2bndy5 in [`40de9f3`](https://github.com/nRF24/pyRF24/commit/40de9f33b82ca245116ca66706a89122813a8a81)
- Don't update docs when CI run on PRs by \@2bndy5 in [`1c00e8c`](https://github.com/nRF24/pyRF24/commit/1c00e8cea58bb87a73acbe962d52afa79eb42398)
- Improve stubs and some docs by \@2bndy5 in [`aa750e8`](https://github.com/nRF24/pyRF24/commit/aa750e8c2089928448831595518b7b4d82445275)
- Ok fix last docs change by \@2bndy5 in [`557f9d0`](https://github.com/nRF24/pyRF24/commit/557f9d01d73f6eed7d2ca2cd894faecc288fbbc8)
- Update docs for theme changes by \@2bndy5 in [`797fdcb`](https://github.com/nRF24/pyRF24/commit/797fdcb04ff11e80493d197c2b4d879e7ae92ef5)
- Doc updates regarding sphinx-immaterial theme by \@2bndy5 in [#7](https://github.com/nRF24/pyRF24/pull/7)
- [docs update] rename logo img by \@2bndy5 in [`c843c7d`](https://github.com/nRF24/pyRF24/commit/c843c7d3dca0e7c83796da88f3401128c3ef7b4b)
- Only update hosted docs if pushed to main branch by \@2bndy5 in [`8c1a69b`](https://github.com/nRF24/pyRF24/commit/8c1a69b0e4565bf5ac9d2e515b3b2c3829280a13)
- Update building docs info & hide ToC on landing pg by \@2bndy5 in [`07fc636`](https://github.com/nRF24/pyRF24/commit/07fc63681ba1c12991e4d83f532b7d440d263093)
- Update network_flags docstr by \@2bndy5 in [`329a883`](https://github.com/nRF24/pyRF24/commit/329a883b5b69086d76d0ae9514e727a6406e7748)
- Autodoc enums & some more spelling fixes by \@2bndy5 in [`804f21d`](https://github.com/nRF24/pyRF24/commit/804f21d4be3949557f8ad3368d6aff02907b4a97)
- Manually doc header.next_id by \@2bndy5 in [`772ba53`](https://github.com/nRF24/pyRF24/commit/772ba5398840ad50aa4274bdc3976c558fca5b54)
- Don't document toString() (its a duplicate) by \@2bndy5 in [`12bf9e4`](https://github.com/nRF24/pyRF24/commit/12bf9e4dc585770fa0b50efb602a9daeb4a1f7a8)

### <!-- 9 --> 🗨️ Changed

- Initial commit by \@TMRh20 in [`9f107ae`](https://github.com/nRF24/pyRF24/commit/9f107ae0d662bd6f154c410c1c550d9d54c1072c)
- Init commit by \@2bndy5 in [`f0870f2`](https://github.com/nRF24/pyRF24/commit/f0870f2c76a4b5ffa7d642732568ca509b720c62)
- CnP error in workflow by \@2bndy5 in [`7146839`](https://github.com/nRF24/pyRF24/commit/7146839f1d4c277cd5ad9259973c870b69476200)
- Install RPi.GPIO via pip by \@2bndy5 in [`7be412a`](https://github.com/nRF24/pyRF24/commit/7be412a390bc351af38ab7d47688714da350fc63)
- Use apt-get in workflow by \@2bndy5 in [`84361b4`](https://github.com/nRF24/pyRF24/commit/84361b46b792114015b0e1b83053fdc93f590638)
- Ensure wheel is installed via pip by \@2bndy5 in [`2561085`](https://github.com/nRF24/pyRF24/commit/2561085c5d73cfcce0e093bc7d428b33fafbd321)
- Merge pull request \#2 from 2bndy5/main by \@TMRh20 in [#2](https://github.com/nRF24/pyRF24/pull/2)
- (+) info on "sphinx cmd not found" by \@2bndy5 in [`50825e6`](https://github.com/nRF24/pyRF24/commit/50825e6c64b50a7e92c0a9144d7293b1f74bb038)
- Update pyproject.toml by \@2bndy5 in [`067dc05`](https://github.com/nRF24/pyRF24/commit/067dc058ca69d143d8a2d465734005d36cc761ee)
- Update submodules by \@2bndy5 in [`4956863`](https://github.com/nRF24/pyRF24/commit/49568633fbe930500a347588f892c1f51a5a274c)
- Incomplete conversion of pyRF24.cpp by \@2bndy5 in [`07b444f`](https://github.com/nRF24/pyRF24/commit/07b444f6fbd9aad5b306a9c88ab037ef566a7a73)
- preparing for a test build by \@2bndy5 in [`0c1e49b`](https://github.com/nRF24/pyRF24/commit/0c1e49b5f16892fb1c9a18385f9f48cbc6d32795)
- Move RF24 submodule by \@2bndy5 in [`289020a`](https://github.com/nRF24/pyRF24/commit/289020aee5b6660a1a4bbd08f5cbe4b5d135de38)
- Re-add RF24 submodule by \@2bndy5 in [`41b0df7`](https://github.com/nRF24/pyRF24/commit/41b0df7c2cb5c8df4324e43b101b0132eb2e4c1d)
- Wrappers re-written by \@2bndy5 in [`aaa6084`](https://github.com/nRF24/pyRF24/commit/aaa60849ed8287c6f81da1f5d5b69a6d36cc8591)
- Update build.yml, gitignore, & submodules' pinned commits by \@2bndy5 in [`97e7e39`](https://github.com/nRF24/pyRF24/commit/97e7e397cb61b230392c8bf5ba03bfbea30e79f0)
- Ignore Makefiles for this repo by \@2bndy5 in [`9d9a14d`](https://github.com/nRF24/pyRF24/commit/9d9a14dcf5f494f9bd9db65ed2218327ad8288a9)
- Pyrf24.core module builds by \@2bndy5 in [`cdd07e8`](https://github.com/nRF24/pyRF24/commit/cdd07e8578ebf9027c5d2cb559f6f76f43bf32cd)
- All wrappers now build with CMake by \@2bndy5 in [`de85b9e`](https://github.com/nRF24/pyRF24/commit/de85b9e164c7d66094f6318254e2c93772e6336e)
- Don't thin-wrap RF24NetworkHeader::toString() by \@2bndy5 in [`fe4561b`](https://github.com/nRF24/pyRF24/commit/fe4561b2742025a71f4a2694e805bb89d4f1cec5)
- Need to install twine to check distribution by \@2bndy5 in [`1fa8e72`](https://github.com/nRF24/pyRF24/commit/1fa8e722f93a4c7d1d2aac7b4971372df7f87235)
- Update actions/checkout to v2 by \@2bndy5 in [`ad2cd06`](https://github.com/nRF24/pyRF24/commit/ad2cd0683210e074fff8c6f7786e6d8d667524b0)
- Long awaited update by \@2bndy5 in [`4a7c1e5`](https://github.com/nRF24/pyRF24/commit/4a7c1e5c84f229c3ed072b8e5f833b11530712bd)
- Create pylint conf; ignore consider-using-f-string by \@2bndy5 in [`00c00b0`](https://github.com/nRF24/pyRF24/commit/00c00b0ce797310dd7b25e8cdc0fa50fcfe7efd9)
- Pylint conf not being used??? by \@2bndy5 in [`87541f1`](https://github.com/nRF24/pyRF24/commit/87541f1f4d3f888d7c23921f64c92ea25dcbd23b)
- Implicitly convert pyObj to char* buffer by \@2bndy5 in [`939f316`](https://github.com/nRF24/pyRF24/commit/939f316bb4be971ffae93b48ce174af8f9472651)
- Implicitly convert pipe addr to uint8_t buffers by \@2bndy5 in [`d81285e`](https://github.com/nRF24/pyRF24/commit/d81285ec705e885a412e76aae8b6b04bb2a5b177)
- Fcast char* to bytearray in read() by \@2bndy5 in [`d1ff134`](https://github.com/nRF24/pyRF24/commit/d1ff1349bb5f69c04b6bd7a66829ce00a98aabb2)
- Read() return reference by \@2bndy5 in [`7542250`](https://github.com/nRF24/pyRF24/commit/75422505080ddd9cbeb02f039212d8e6aa7209f1)
- [read()] don't delete ptr before returning ref by \@2bndy5 in [`3d68ea3`](https://github.com/nRF24/pyRF24/commit/3d68ea38f3caad5c654352b54fb09bc29a6675ee)
- [read()] don't return local ref by \@2bndy5 in [`6c5743c`](https://github.com/nRF24/pyRF24/commit/6c5743cebcdc92bcdba2c51f5543a5b9506cfb9b)
- Forgot about null byte in char* by \@2bndy5 in [`14349e5`](https://github.com/nRF24/pyRF24/commit/14349e5ec5c6c2d61725e537f6fa469209a35a7a)
- [read()] try returning the object directly by \@2bndy5 in [`22c6d9b`](https://github.com/nRF24/pyRF24/commit/22c6d9b56ebb2458865ab5f2495df09b279eabe1)
- [read()] try using python C API only by \@2bndy5 in [`5b161cf`](https://github.com/nRF24/pyRF24/commit/5b161cf5707b6bcc2f326541c57a48680e29d9d7)
- Steal the ref ptr by \@2bndy5 in [`100167e`](https://github.com/nRF24/pyRF24/commit/100167e0166006edd4020aa1be3b2b53b793fdb4)
- Read() convert to std:string then return bytearray by \@2bndy5 in [`622e3dc`](https://github.com/nRF24/pyRF24/commit/622e3dc7eaa6e7f47aa9e4d0030900261594425e)
- Manually increment ref counter by \@2bndy5 in [`45704d0`](https://github.com/nRF24/pyRF24/commit/45704d06d1f60a0f95884abfba11ef96c14f28aa)
- Pass buffer to read() w/o deref-ing ptr by \@2bndy5 in [`ce2f4d4`](https://github.com/nRF24/pyRF24/commit/ce2f4d4053d62e41ff3f1fa339a81ca9806395a4)
- RF24NetWrapper.__init__() takes RF24Wrapper obj by \@2bndy5 in [`ccf47f0`](https://github.com/nRF24/pyRF24/commit/ccf47f049c028874dccdc36eb453bd39f22d6a70)
- RF24MeshWrapper.__init__() takes RF24*Wrapper objs by \@2bndy5 in [`9c5eb54`](https://github.com/nRF24/pyRF24/commit/9c5eb544bcd569ee4872735cb3ff08b405ea528a)
- Net & mesh wrappers properly take py buf objects by \@2bndy5 in [`0c18203`](https://github.com/nRF24/pyRF24/commit/0c182033cc85473e73c8b9b142818844c5b8f746)
- Fill out type hinting; revise examples by \@2bndy5 in [`a029c5d`](https://github.com/nRF24/pyRF24/commit/a029c5df9740a355f12c10633728f340217208d9)
- Use git version tags; update to latest RF24 API by \@2bndy5 in [`92a7e2b`](https://github.com/nRF24/pyRF24/commit/92a7e2bb4bb7928e76ba1b3260f6286875e128f2)
- Yml gotcha (again) by \@2bndy5 in [`b4f5d75`](https://github.com/nRF24/pyRF24/commit/b4f5d756ace58f80fbcf2da77512f4fd8361fbbf)
- Missed a f-string prospect in IRQ example by \@2bndy5 in [`53571e8`](https://github.com/nRF24/pyRF24/commit/53571e8a5cbd3556b9931ad9fa9c7b741dcc1664)
- CI fetch all when checkout repo by \@2bndy5 in [`216c001`](https://github.com/nRF24/pyRF24/commit/216c001634b14e932b1d10fc82f4a46517e705f2)
- Clang-format, fix some pybind casting by \@2bndy5 in [`8b50a99`](https://github.com/nRF24/pyRF24/commit/8b50a99c64db89d17d89091e40da12648ab54f4e)
- Thin wrap set_radiation by \@2bndy5 in [`a6e0474`](https://github.com/nRF24/pyRF24/commit/a6e0474b92c22045e3769952a3792291ee5538e0)
- Expose most of RF24Network API by \@2bndy5 in [`4bc11d4`](https://github.com/nRF24/pyRF24/commit/4bc11d44ce616d79f07cc65516a8c58c47041722)
- Update examples and rf24 stub file by \@2bndy5 in [`d8d432a`](https://github.com/nRF24/pyRF24/commit/d8d432a86ef2ea816f0c69f434a5e59d8213dc27)
- Use explicit len of buf when casting to bytearray by \@2bndy5 in [`9d5dd6b`](https://github.com/nRF24/pyRF24/commit/9d5dd6bbe38a330e09ecacea2a393a9aa0aed1c8)
- More example fixes by \@2bndy5 in [`00cf603`](https://github.com/nRF24/pyRF24/commit/00cf603a58a84c9d4d93f26f1c8f32e0bd4218ae)
- Hopefully last fix for RF24 examples by \@2bndy5 in [`3bf36c9`](https://github.com/nRF24/pyRF24/commit/3bf36c9bca7da2b3e5c6510ed83cb67bfc2e0eea)
- Fun with pure python by \@2bndy5 in [`578efeb`](https://github.com/nRF24/pyRF24/commit/578efeb2b6f192440987ab103f7850263cbb9cbd)
- Test round 2 prep by \@2bndy5 in [`9efc7fd`](https://github.com/nRF24/pyRF24/commit/9efc7fd743761636ebe8417740ba090233fdcc81)
- [fake_ble] don't pass None as pins to super.begin by \@2bndy5 in [`bff0caa`](https://github.com/nRF24/pyRF24/commit/bff0caa9268bc7572099a8138c6d61825c8d0c73)
- Ammend ble example by \@2bndy5 in [`060c0eb`](https://github.com/nRF24/pyRF24/commit/060c0eba08e1b409439805895914f9276226c7db)
- FakeBLE only overrides what it needs to by \@2bndy5 in [`cc8485f`](https://github.com/nRF24/pyRF24/commit/cc8485f8a2c45397de2763a2429c701409e80575)
- Make FakeBLE a wrapper class (not derivative) by \@2bndy5 in [`b5b0550`](https://github.com/nRF24/pyRF24/commit/b5b055007522f6efcd233aeb51243ffef06009ed)
- [FakeBLE] missed a couple RF24 specific API calls by \@2bndy5 in [`cb835ac`](https://github.com/nRF24/pyRF24/commit/cb835acdb8ba3dc397876240ce583b8ffc22c094)
- Enable debugging options from cli by \@2bndy5 in [`bc6d254`](https://github.com/nRF24/pyRF24/commit/bc6d254b6701205ec82e3283266ae88f23c5fef1)
- Ensure primary mode is correct in ble example by \@2bndy5 in [`85dad77`](https://github.com/nRF24/pyRF24/commit/85dad772232ae2f7972016cf6aa6735ab1688b0d)
- Cmake mesh debug macros; RF24.begin mesh examples by \@2bndy5 in [`438e08e`](https://github.com/nRF24/pyRF24/commit/438e08ea3360ff7b06b7c78c766aa108ee8bc756)
- Cast wrappers as their base to Mesh c'tor by \@2bndy5 in [`1a3e941`](https://github.com/nRF24/pyRF24/commit/1a3e94115319efa0b6d0c8586304419403c091d5)
- Hard code some debug statements in bindings by \@2bndy5 in [`c9bb8a2`](https://github.com/nRF24/pyRF24/commit/c9bb8a2dd2a2d822519a57b16ca47886bbd72782)
- Bump submods RF24Mesh->master & pybind11->v2.9.1 by \@2bndy5 in [`2dea367`](https://github.com/nRF24/pyRF24/commit/2dea36755ddc25f25170837d3d83127adb176c8c)
- New apply_flags() in cmake by \@2bndy5 in [`94aa66d`](https://github.com/nRF24/pyRF24/commit/94aa66dfd9d7e95fcfa06863872885cb35e1df8e)
- Update mesh submodule and generic network test by \@2bndy5 in [`a3f9cfb`](https://github.com/nRF24/pyRF24/commit/a3f9cfb0ce96717bbcf038d23a0f3b7b8df2caeb)
- Oops that property is static; revise example again by \@2bndy5 in [`7e69375`](https://github.com/nRF24/pyRF24/commit/7e69375e7dc6e6a3290c6dff6c0f050b59c397f8)
- If logic in example prompt by \@2bndy5 in [`d120bcb`](https://github.com/nRF24/pyRF24/commit/d120bcbeae95bdbdf5849eceb57a19925d02364a)
- Use python v3.9 in CI workflow by \@2bndy5 in [`5a57478`](https://github.com/nRF24/pyRF24/commit/5a5747802655d75d262b8eb804d15483f1676e7f)
- Metadata pkg not consistent among versions of py by \@2bndy5 in [`a2e8d83`](https://github.com/nRF24/pyRF24/commit/a2e8d8306d86feb50dee1ebc39128a78fc65776a)
- Install dot tool for CI by \@2bndy5 in [`a4de7ec`](https://github.com/nRF24/pyRF24/commit/a4de7ecda4e70bfc7b41fd756343a3c2c2bd8820)
- Update README by \@2bndy5 in [`b142117`](https://github.com/nRF24/pyRF24/commit/b1421173f299d2336ca2e7e016cfa79778eeaeb2)
- Reviewed ble example by \@2bndy5 in [`072b602`](https://github.com/nRF24/pyRF24/commit/072b602acc649c4fb1ce4c204f7fb679a2fee4ab)
- Modify generic_net_test.py and rf24_net stub by \@2bndy5 in [`602e40a`](https://github.com/nRF24/pyRF24/commit/602e40a3ab61f6eaa986b8929284002d6d1a0306)
- Generic_net_test.py allow strict timeout in idle() by \@2bndy5 in [`42b68f4`](https://github.com/nRF24/pyRF24/commit/42b68f41e5e15dbd194dee18708ff84543a4309f)
- Bindings pass buffers by value not reference by \@2bndy5 in [`607ed29`](https://github.com/nRF24/pyRF24/commit/607ed2930f8902a5952e7c7c3a2221d9c98c461a)
- Generic net test: cleaner starting prompts by \@2bndy5 in [`631eaf7`](https://github.com/nRF24/pyRF24/commit/631eaf7ac3c17893fa5dfc523eed388a57a958ca)
- Self review changes by \@2bndy5 in [`359a262`](https://github.com/nRF24/pyRF24/commit/359a2623b13de266a4cafc29b28ec63294ccc198)
- Install only stubs for non-linux by \@2bndy5 in [`c6fafd2`](https://github.com/nRF24/pyRF24/commit/c6fafd2e433b9a6d96d5b1d66be6bbe4956464a2)
- Expose addrList & addrListStruct in RF24Mesh by \@2bndy5 in [`2233d44`](https://github.com/nRF24/pyRF24/commit/2233d44da75e827d9cc03c13d2237e7601dfaaa4)
- Merge pull request \#5 from 2bndy5/add-submodules by \@TMRh20 in [#5](https://github.com/nRF24/pyRF24/pull/5)
- Convert line endings to LF by \@2bndy5 in [`6ecd039`](https://github.com/nRF24/pyRF24/commit/6ecd0391b8c67d273fe0f0135ccaa3a9ce1c7cb7)
- Test build ok by \@2bndy5 in [`5d7e431`](https://github.com/nRF24/pyRF24/commit/5d7e431f090ed0b385bd5edafa87fc8a1c4218f5)
- Upgrade status to beta by \@2bndy5 in [`4356095`](https://github.com/nRF24/pyRF24/commit/4356095afec62ac0fc0c548ff2f9f1c44f7429af)
- Pybind11 can't overload a property with a function by \@2bndy5 in [`1782ce8`](https://github.com/nRF24/pyRF24/commit/1782ce865154c388ce17f440a8469a9fc1308742)
- Update readme about API diffs & stub files by \@2bndy5 in [`854fb87`](https://github.com/nRF24/pyRF24/commit/854fb87fe843e80853551f0b36bef3c67e161822)
- Try to fix logo img (somehow currupted on remote) by \@2bndy5 in [`64ce888`](https://github.com/nRF24/pyRF24/commit/64ce88857bdda14ed5a96a30321c3267089fbff6)
- Use jpg instead of png for logo img by \@2bndy5 in [`43cfc49`](https://github.com/nRF24/pyRF24/commit/43cfc493531023635d474f04cc11a0a417501a32)
- Updated networking examples (ported from old) by \@2bndy5 in [`39377e0`](https://github.com/nRF24/pyRF24/commit/39377e0c9a74a5048c9ed233d2a3b1842a3827f8)
- Its a bool attr not a func by \@2bndy5 in [`0466f41`](https://github.com/nRF24/pyRF24/commit/0466f41547ec8b56446a205f73aa066cf9f23d4d)
- Oops wrong line concerning lsat commit by \@2bndy5 in [`90eafc1`](https://github.com/nRF24/pyRF24/commit/90eafc1abf10139dfe093ad72dc362dd74e4d427)

[0.2.0]: https://github.com/nRF24/pyRF24/compare/9f107ae0d662bd6f154c410c1c550d9d54c1072c...v0.2.0

Full commit diff: [`9f107ae...v0.2.0`][0.2.0]

## New Contributors
* \@2bndy5 made their first contribution in [#11](https://github.com/nRF24/pyRF24/pull/11)
* \@TMRh20 made their first contribution in [#9](https://github.com/nRF24/pyRF24/pull/9)
<!-- generated by git-cliff -->
