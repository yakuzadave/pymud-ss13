# 🤖 Agent Development Guide

**Project:** pymud-ss13  
**Generated:** 2025-06-16 21:21:18  
**For:** New team member onboarding
**Repository:** https://github.com/yakuzadave/pymud-ss13
**Commit:** 9637749
**Branch:** main

---

## 📈 Recent Changes (Last 5 Commits)

The following commits show recent development activity. Review these to understand current work:

- **9637749** (23 seconds ago by Katharsis): updated script and workflow
- **9d4497d** (9 minutes ago by Katharsis): Add script to add context to AGENTS.md
- **baf0d2e** (13 minutes ago by Katharsis): Merge pull request #134 from yakuzadave/codex/add-get_player_inventory-method-and-initialize-inventory
- **33d98a7** (14 minutes ago by Katharsis): docs: track mudpy interface progress
- **47d7139** (27 minutes ago by Katharsis): Merge pull request #133 from yakuzadave/z1kd58-codex/fix--status--command-execution-error

### 🔍 Detailed Recent Changes

#### Commit 9637749 - updated script and workflow
**Author:** Katharsis <34697131+yakuzadave@users.noreply.github.com>
**Date:** 2025-06-16 21:20:55
**Message:**

---
#### Commit 9d4497d - Add script to add context to AGENTS.md
**Author:** Katharsis <34697131+yakuzadave@users.noreply.github.com>
**Date:** 2025-06-16 21:12:39
**Message:**

---
#### Commit baf0d2e - Merge pull request #134 from yakuzadave/codex/add-get_player_inventory-method-and-initialize-inventory
**Author:** Katharsis <34697131+yakuzadave@users.noreply.github.com>
**Date:** 2025-06-16 14:07:54
**Message:**
Add getter for inventory and track interface progress
---

### 📁 Files Modified Recently

- .github/workflows/update-agents-md.yml
- AGENTS.md
- agent_write.sh
- data/aliases/135333523153856.yaml
- docs/mudpy_interface_progress.md
- mudpy_interface.py


## 🧪 Test Results

**Status:** ✅ PASSED  
**Run Date:** 2025-06-16 21:21:27

### Test Output
```
============================= test session starts ==============================
platform linux -- Python 3.13.4, pytest-8.4.0, pluggy-1.6.0
benchmark: 5.1.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /home/runner/work/pymud-ss13/pymud-ss13
configfile: pyproject.toml
plugins: metadata-3.1.1, benchmark-5.1.0, html-4.1.1, anyio-4.9.0, cov-6.2.1
collected 127 items

tests/test_action_queue.py .                                             [  0%]
tests/test_advanced_antagonists.py ......                                [  5%]
tests/test_advanced_chemistry.py ..                                      [  7%]
tests/test_ai_gameplay.py .                                              [  7%]
tests/test_alias_commands.py ..                                          [  9%]
tests/test_aliases.py ..                                                 [ 11%]
tests/test_antag_command.py .                                            [ 11%]
tests/test_antagonists.py ..                                             [ 13%]
tests/test_atmos_sim.py ..                                               [ 14%]
tests/test_bartender.py .                                                [ 15%]
tests/test_botany_kitchen.py ....                                        [ 18%]
tests/test_botany_mechanics.py ....                                      [ 22%]
tests/test_cargo.py ........                                             [ 28%]
tests/test_chemical_reactions.py ..                                      [ 29%]
tests/test_chemistry.py ....                                             [ 33%]
tests/test_circuit_system.py ...                                         [ 35%]
tests/test_cli.py .                                                      [ 36%]
tests/test_combat_system.py .                                            [ 37%]
tests/test_communications.py .                                           [ 37%]
tests/test_construction_system.py ..                                     [ 39%]
tests/test_containers.py ..                                              [ 40%]
tests/test_cook_command.py .                                             [ 41%]
tests/test_door_id_card_access.py ..                                     [ 43%]
tests/test_doors.py .                                                    [ 44%]
tests/test_environmental_protection.py .                                 [ 44%]
tests/test_equipment.py .                                                [ 45%]
tests/test_explosive_decompression.py .                                  [ 46%]
tests/test_fire_system.py .                                              [ 47%]
tests/test_genetics.py ...                                               [ 49%]
tests/test_jobs.py ....                                                  [ 52%]
tests/test_maintenance_system.py ..                                      [ 54%]
tests/test_manifest_and_login.py ..                                      [ 55%]
tests/test_medical.py ...                                                [ 58%]
tests/test_nutrition.py .                                                [ 59%]
tests/test_pathfinding.py ..                                             [ 60%]
tests/test_performance.py .                                              [ 61%]
tests/test_performance_monitor.py .                                      [ 62%]
tests/test_persistence.py ...                                            [ 64%]
tests/test_physics.py .                                                  [ 65%]
tests/test_player_loading.py .                                           [ 66%]
tests/test_plumbing_system.py ..                                         [ 67%]
tests/test_power_system.py ..                                            [ 69%]
tests/test_random_events.py .....                                        [ 73%]
tests/test_replica_pod.py .                                              [ 74%]
tests/test_research.py ..                                                [ 75%]
tests/test_robotics.py ....                                              [ 78%]
tests/test_roles.py .........                                            [ 85%]
tests/test_room_status.py .                                              [ 86%]
tests/test_security_system.py .                                          [ 87%]
tests/test_silicon.py ...                                                [ 89%]
tests/test_space_exploration.py ...                                      [ 92%]
tests/test_spatial.py ...                                                [ 94%]
tests/test_status_command.py .                                           [ 95%]
tests/test_structure.py .                                                [ 96%]
tests/test_surgery.py ...                                                [ 98%]
tests/test_who.py .                                                      [ 99%]
tests/test_world_load.py .                                               [100%]

================================ tests coverage ================================
_______________ coverage: platform linux, python 3.13.4-final-0 ________________

Name                                     Stmts   Miss  Cover   Missing
----------------------------------------------------------------------
action_queue.py                             10      0   100%
cli.py                                      16      2    88%   16-17
combined_server.py                          20     20     0%   5-40
command_spec.py                             63     19    70%   102-125, 138, 169-173
commands/__init__.py                         0      0   100%
commands/admin.py                           21      1    95%   22
commands/ai.py                              14      9    36%   11-19
commands/aliases.py                         33      9    73%   13-17, 20, 25, 37, 45
commands/antag.py                           39     20    49%   16, 24, 26, 31-49
commands/bartender.py                       15      3    80%   13, 16, 18
commands/basic.py                           26      9    65%   26-37, 56, 62
commands/botanist.py                        75     35    53%   11, 14, 23, 25, 34-42, 52, 54, 63-70, 78-86, 94, 96, 100
commands/cargo.py                           26     22    15%   8-34
commands/chef.py                            15      3    80%   13, 16, 18
commands/chemist.py                         86     21    76%   13, 16, 18, 27, 30, 32, 37, 41, 58, 61, 63, 68, 72, 74, 94, 97, 101, 104, 106, 113-114
commands/circuit.py                         25     21    16%   15-35
commands/comms.py                           34     26    24%   7-14, 19-26, 31-40
commands/debug.py                           88     73    17%   29-51, 68-87, 103-128, 144-173, 190-219
commands/doctor.py                          32      7    78%   13, 16, 18, 22, 25, 42, 45
commands/engineer.py                        77     17    78%   14, 17, 27, 30, 35, 44, 53, 56, 58, 63, 72, 74, 86, 89, 93, 95, 100
commands/interaction.py                    134    110    18%   14-55, 74-86, 104-114, 130-142, 160-172, 180-194, 210-214, 230-234, 250-254, 260-287
commands/inventory.py                      149     78    48%   20, 25, 29-34, 40, 45, 52, 57-84, 91, 96-98, 104-144, 149-151, 156-158, 163, 171, 177, 182, 188, 196, 208
commands/job.py                             31     26    16%   11-43
commands/movement.py                        88     45    49%   34, 37, 44, 46, 48, 50, 52, 54, 58, 63, 70, 86, 90, 97, 126-182
commands/observation.py                    184    162    12%   31, 34-98, 113-150, 165-270, 284-339, 345-357
commands/requisition.py                     25     19    24%   10-31
commands/research.py                        17     11    35%   8-12, 18-23
commands/security.py                        75     49    35%   14, 17, 32-42, 48-56, 62-71, 77-86, 92-94, 100-108, 114-117
commands/social.py                         109     95    13%   26-56, 71-109, 125-172, 188-237, 252-270
commands/system.py                          66     24    64%   30-39, 58-68, 85-98, 111, 116, 123, 125, 137-139, 151
components/__init__.py                      20      0   100%
components/access.py                        15      5    67%   18-26, 29
components/ai.py                            47      3    94%   59, 75, 96
components/camera.py                        18      8    56%   16-18, 21-22, 25-26, 29
components/circuit.py                       26      5    81%   41-44, 47
components/container.py                     90     36    60%   35, 42-43, 49, 65, 80, 84, 88-95, 99-109, 112-125, 128-140, 145, 147
components/door.py                          81     14    83%   57, 105, 127, 131, 153, 157, 169, 171, 182-186, 195
components/fluid.py                         34     11    68%   22, 24, 30, 32, 39-44, 47
components/id_card.py                        7      1    86%   14
components/item.py                         101     33    67%   54, 66-72, 85-87, 100, 104, 125-127, 148, 172, 186-208, 217
components/maintenance.py                   39      2    95%   33, 57
components/motion_sensor.py                 14      6    57%   15-18, 21, 26
components/npc.py                           68     19    72%   41, 45, 48, 51, 54-56, 61, 63-71, 73-74, 85, 105-106, 119-121
components/player.py                       218     55    75%   91, 115, 144, 149, 152, 166, 214, 233, 237, 256, 260, 272-273, 302, 313-316, 339, 346, 349, 364-407, 417, 424, 430, 445, 474-478
components/power_consumer.py                42      3    93%   52, 62, 68
components/replica_pod.py                   30      4    87%   20, 23, 25, 32
components/room.py                          42     25    40%   54, 64-65, 79-83, 92-103, 112-114, 126-130, 139
components/structure.py                     42      3    93%   43, 60, 72
connection.py                               68     68     0%   6-193
engine.py                                   52     10    81%   105, 130-131, 149-150, 154-159
events.py                                   53     20    62%   89-90, 108-135, 145, 158
integration.py                             127     24    81%   64, 67, 72, 76, 80, 84, 105-106, 210-211, 217, 230-231, 242-247, 258-264, 293
mod_manager.py                              80     10    88%   47-48, 73-74, 93, 100-101, 106, 117-118
mods/example_mod/scripts/example.py          1      0   100%
mud_server.py                              194     99    49%   52-53, 98-154, 204, 233, 236-237, 239, 253-255, 309-312, 330-358, 371-394, 407-430, 444-467, 483-502, 510-519, 527-531, 548, 553-557
mud_websocket_server.py                    183    183     0%   8-406
mudpy_interface.py                         396    257    35%   250-253, 351-400, 419-423, 432, 435-436, 454, 472-569, 582-586, 598-606, 618-644, 648-667, 681, 687, 691, 706, 710, 720, 733-778, 791-861, 875-909, 922-971, 989-1023, 1053, 1065-1067, 1074, 1096-1100
parser.py                                  114     31    73%   53-54, 85-86, 104-107, 139-175, 205, 226-227, 243, 252
pathfinding.py                              29      4    86%   18, 30, 33, 46
performance.py                              43      8    81%   40, 57-64
persistence.py                             188     92    51%   19-31, 36-71, 75-103, 107-131, 137-138, 143, 173-177, 180, 184-187, 255-256, 261-263, 272-273, 284-289, 299-300
random_events.py                            35     10    71%   20-21, 23-28, 33, 46
run_server.py                               63     63     0%   8-140
script_manager.py                           77     77     0%   6-281
server.py                                  175    175     0%   6-475
settings.py                                 16     16     0%   6-41
spatial.py                                  59      3    95%   34, 64-65
start_server.py                             95     95     0%   7-192
system_loops.py                             22     22     0%   1-29
systems/__init__.py                         28      0   100%
systems/advanced_antagonists.py            111     13    88%   37, 60-67, 84-85, 97-98, 114-115, 147, 195
systems/advanced_chemistry.py               77     11    86%   37-40, 45, 78, 83, 106, 114, 132, 137
systems/ai.py                                7      5    29%   8-12
systems/antagonists.py                      53     13    75%   59, 70-77, 93, 103-105
systems/atmos.py                           194     84    57%   66-67, 81-82, 90, 94, 106, 110, 116-117, 127, 129, 149-178, 188-199, 209, 215-218, 222, 226-229, 231, 235-238, 242, 246-249, 253, 256-259, 261, 264-266, 270, 328-329, 343-345, 350, 367-369, 374, 387-388, 398-401
systems/atmosphere.py                        1      0   100%
systems/bar.py                              61      4    93%   50, 53, 59, 86
systems/botany.py                          155     41    74%   65, 71, 77, 80-85, 91, 114, 117-133, 143, 150-167, 173, 187, 190
systems/cargo.py                           137     27    80%   40, 51, 100, 107-108, 155-160, 164-169, 184-188, 203-204, 207-208, 228
systems/chemical_reactions.py               66      4    94%   46, 52, 85, 97
systems/chemistry.py                        54      7    87%   22-23, 39, 46, 49, 56, 70
systems/circuits.py                         56     11    80%   42, 45, 56, 61-65, 69, 73, 91
systems/combat.py                           46      2    96%   48, 51
systems/communications.py                  115     30    74%   71, 79-80, 84-86, 102, 104, 106, 110-112, 117, 130, 138, 144-154, 169, 193, 204, 221-223, 232-235, 245
systems/construction.py                     97      7    93%   57, 66, 84, 93, 96, 98, 177
systems/disease.py                          64     17    73%   23, 26, 29, 35-43, 49, 52, 60, 74, 86
systems/fire.py                             34      2    94%   33, 40
systems/gas_sim.py                         124     31    75%   98, 111-115, 120, 130, 133, 152-153, 158, 161-181
systems/genetics.py                         94      7    93%   44-45, 66, 80, 107, 111, 114
systems/jobs.py                            216     21    90%   86, 138, 158, 185, 195-196, 219-237, 269-273, 294, 303-306
systems/kitchen.py                          62      4    94%   54, 57, 63, 85
systems/maintenance.py                      36      5    86%   31, 35, 38, 44, 55
systems/npc_ai.py                           31     12    61%   27, 31, 35-44
systems/physics.py                          41     12    71%   37, 40, 45, 50-58
systems/plumbing.py                         49      9    82%   29-30, 38, 45, 50, 53, 59, 63, 77
systems/power.py                           236     76    68%   66, 205-211, 229-234, 270-271, 274, 288-289, 297, 301, 318-320, 325-326, 337-344, 354-356, 360-370, 373, 399-414, 448, 460-463, 474-506, 516-518, 528-537
systems/random_events.py                    87     16    82%   46-48, 67-71, 76, 78, 98-99, 104, 107, 122, 134
systems/research.py                         88     12    86%   80, 83, 89, 91, 111, 113, 115, 117, 124, 131-132, 140
systems/robotics.py                        113      5    96%   65, 80, 101, 176, 184
systems/script_engine.py                    72     39    46%   25, 38-50, 54-57, 61, 65-71, 77-87, 96-99, 105-106, 112, 125-126, 144-151
systems/security.py                        119     29    76%   108-113, 134, 149-150, 157-158, 163-164, 169-170, 183, 185-189, 201-205, 210, 215, 226
systems/space_exploration.py               158     16    90%   28-29, 44-45, 121, 149, 151, 160, 216, 220-223, 235, 240, 252
systems/surgery.py                          61      9    85%   35, 40, 44, 47, 50, 67, 70, 74, 102
tests/ai_tools.py                           12      0   100%
tests/test_action_queue.py                  21      0   100%
tests/test_advanced_antagonists.py          43      0   100%
tests/test_advanced_chemistry.py            16      0   100%
tests/test_ai_gameplay.py                   27      0   100%
tests/test_alias_commands.py                32      0   100%
tests/test_aliases.py                       33      0   100%
tests/test_antag_command.py                 24      0   100%
tests/test_antagonists.py                   21      0   100%
tests/test_atmos_sim.py                     25      0   100%
tests/test_bartender.py                     31      0   100%
tests/test_botany_kitchen.py                74      0   100%
tests/test_botany_mechanics.py              54      0   100%
tests/test_cargo.py                         59      0   100%
tests/test_chemical_reactions.py            34      0   100%
tests/test_chemistry.py                     75      0   100%
tests/test_circuit_system.py                30      0   100%
tests/test_cli.py                            5      0   100%
tests/test_combat_system.py                 26      0   100%
tests/test_communications.py                21      0   100%
tests/test_construction_system.py           35      0   100%
tests/test_containers.py                    32      0   100%
tests/test_cook_command.py                  33      0   100%
tests/test_door_id_card_access.py           51      0   100%
tests/test_doors.py                         21      0   100%
tests/test_environmental_protection.py      15      0   100%
tests/test_equipment.py                     37      0   100%
tests/test_explosive_decompression.py       10      0   100%
tests/test_fire_system.py                   11      0   100%
tests/test_genetics.py                      47      0   100%
tests/test_jobs.py                          62      0   100%
tests/test_maintenance_system.py            32      0   100%
tests/test_manifest_and_login.py            52      0   100%
tests/test_medical.py                       62      0   100%
tests/test_nutrition.py                     21      0   100%
tests/test_pathfinding.py                   48      0   100%
tests/test_performance.py                   13      0   100%
tests/test_performance_monitor.py           14      0   100%
tests/test_persistence.py                   50      0   100%
tests/test_physics.py                       11      0   100%
tests/test_player_loading.py                18      0   100%
tests/test_plumbing_system.py               29      0   100%
tests/test_power_system.py                  38      0   100%
tests/test_random_events.py                 70      0   100%
tests/test_replica_pod.py                   38      0   100%
tests/test_research.py                      25      0   100%
tests/test_robotics.py                      54      0   100%
tests/test_roles.py                        104      0   100%
tests/test_room_status.py                   27      0   100%
tests/test_security_system.py               16      0   100%
tests/test_silicon.py                       42      0   100%
tests/test_space_exploration.py             43      0   100%
tests/test_spatial.py                       43      0   100%
tests/test_status_command.py                16      0   100%
tests/test_structure.py                     14      0   100%
tests/test_surgery.py                       56      0   100%
tests/test_who.py                           19      0   100%
tests/test_world_load.py                    22      0   100%
world.py                                   170     43    75%   48-49, 95, 104-110, 146-149, 153-156, 160-163, 187-188, 221, 223, 225, 227, 234, 241, 251, 304-308, 311, 322-324, 336-349
----------------------------------------------------------------------
TOTAL                                     9704   3060    68%

----------------------------------------------------- benchmark: 1 tests ----------------------------------------------------
Name (time in us)                Min       Max     Mean   StdDev   Median     IQR  Outliers  OPS (Kops/s)  Rounds  Iterations
-----------------------------------------------------------------------------------------------------------------------------
test_command_performance     39.9040  518.4360  45.0469  10.1565  42.9700  4.0480   244;347       22.1991    4793           1
-----------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
============================= 127 passed in 7.45s ==============================
```

### Coverage Summary
```
tests/test_who.py                           19      0   100%
tests/test_world_load.py                    22      0   100%
world.py                                   170     43    75%   48-49, 95, 104-110, 146-149, 153-156, 160-163, 187-188, 221, 223, 225, 227, 234, 241, 251, 304-308, 311, 322-324, 336-349
----------------------------------------------------------------------
TOTAL                                     9704   3060    68%

----------------------------------------------------- benchmark: 1 tests ----------------------------------------------------
Name (time in us)                Min       Max     Mean   StdDev   Median     IQR  Outliers  OPS (Kops/s)  Rounds  Iterations
-----------------------------------------------------------------------------------------------------------------------------
test_command_performance     39.9040  518.4360  45.0469  10.1565  42.9700  4.0480   244;347       22.1991    4793           1
-----------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
```

### Environment Info
```
Python Version: Python 3.13.4
Working Directory: /home/runner/work/pymud-ss13/pymud-ss13
Git Branch: main
Git Remote: https://github.com/yakuzadave/pymud-ss13
```

---

## 🎯 Getting Started Guide

### 🔍 What to Review

1. **Test Results Above**: Check if all tests are passing. If not, these might be good first issues to tackle.

2. **Recent Commits**: Look at the commit history above to understand:
   - What features are being developed
   - What bugs have been fixed recently
   - Coding patterns and conventions used

3. **Modified Files**: The files listed in "Files Modified Recently" are active areas of development.

### 🛠️ Recommended Next Steps

1. **Fix Failing Tests**: If any tests are failing, start by investigating and fixing them.

2. **Code Review**: Review the recent commits to understand the codebase structure and patterns.

3. **Documentation**: Check if any of the recently modified files need documentation updates.

4. **Testing**: Consider adding tests for any code that appears undertested based on coverage reports.

### 🚀 Finding Work

- Look for TODO comments in recently changed files: `grep -r "TODO\|FIXME\|XXX" .`
- Check for issues in the repository's issue tracker
- Look for functions/modules with low test coverage
- Review commit messages for mentions of "WIP" or "partial" implementations

### 🤝 Contributing

Before making changes:
1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Run tests locally: `pytest --cov=.`
3. Check code style (if applicable): `flake8 .` or `black .`
4. Commit with descriptive messages following project conventions

---

**Happy coding! 🎉**

*This file was automatically generated by `generate_agents_md.sh` on 2025-06-16 21:21:27 (GitHub Actions Run #15692219242)*
