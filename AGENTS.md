# 🤖 Agent Development Guide

**Project:** pymud-ss13  
**Generated:** 2025-06-17 05:57:22  
**For:** New team member onboarding
**Repository:** https://github.com/yakuzadave/pymud-ss13
**Commit:** c66d568
**Branch:** main

---

## 📈 Recent Changes (Last 5 Commits)

The following commits show recent development activity. Review these to understand current work:

- **c66d568** (19 seconds ago by Katharsis): Merge pull request #160 from yakuzadave/codex/add-random-event-definitions-and-support
- **b597683** (57 seconds ago by Katharsis): Add conditional random events with severity
- **aea8e63** (84 minutes ago by GitHub Action): 🤖 Auto-update AGENTS.md
- **4d93cbd** (84 minutes ago by Katharsis): Merge pull request #159 from yakuzadave/codex/add-actions-to-commands/consoles.py
- **177f6a9** (85 minutes ago by Katharsis): Add console enhancements and tests

### 🔍 Detailed Recent Changes

#### Commit c66d568 - Merge pull request #160 from yakuzadave/codex/add-random-event-definitions-and-support
**Author:** Katharsis <34697131+yakuzadave@users.noreply.github.com>
**Date:** 2025-06-16 22:57:03
**Message:**

---
#### Commit b597683 - Add conditional random events with severity
**Author:** Katharsis <34697131+yakuzadave@users.noreply.github.com>
**Date:** 2025-06-16 22:56:25
**Message:**

---
#### Commit aea8e63 - 🤖 Auto-update AGENTS.md
**Author:** GitHub Action <action@github.com>
**Date:** 2025-06-17 04:33:03
**Message:**
- Updated from commit: 67b2d74b36627ff787add87e30a5402d6b5b0552
- Triggered by: push
- Branch: main

[skip ci][autogen AGENTS.md]

---

### 📁 Files Modified Recently

- AGENTS.md
- commands/consoles.py
- data/commands.yaml
- data/random_events.yaml
- docs/commands_reference.md
- docs/text_interaction_design.md
- systems/cargo.py
- systems/power.py
- systems/random_events.py
- tests/test_console_commands.py
- tests/test_random_events.py


## 🧪 Test Results

**Status:** ✅ PASSED  
**Run Date:** 2025-06-17 05:57:32

### Test Output
```
============================= test session starts ==============================
platform linux -- Python 3.13.4, pytest-8.4.0, pluggy-1.6.0
benchmark: 5.1.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /home/runner/work/pymud-ss13/pymud-ss13
configfile: pyproject.toml
plugins: metadata-3.1.1, benchmark-5.1.0, html-4.1.1, anyio-4.9.0, cov-6.2.1
collected 154 items

tests/test_action_queue.py .                                             [  0%]
tests/test_advanced_antagonists.py ......                                [  4%]
tests/test_advanced_chemistry.py ..                                      [  5%]
tests/test_ai_gameplay.py .                                              [  6%]
tests/test_ai_system.py ..                                               [  7%]
tests/test_alias_commands.py ..                                          [  9%]
tests/test_aliases.py ..                                                 [ 10%]
tests/test_antag_command.py .                                            [ 11%]
tests/test_antagonists.py ..                                             [ 12%]
tests/test_atmos_sim.py ..                                               [ 13%]
tests/test_bartender.py .                                                [ 14%]
tests/test_botany_kitchen.py ....                                        [ 16%]
tests/test_botany_mechanics.py ....                                      [ 19%]
tests/test_cargo.py ..........                                           [ 25%]
tests/test_chemical_reactions.py ..                                      [ 27%]
tests/test_chemistry.py ....                                             [ 29%]
tests/test_circuit_system.py ...                                         [ 31%]
tests/test_cli.py .                                                      [ 32%]
tests/test_combat_system.py .                                            [ 33%]
tests/test_communications.py .                                           [ 33%]
tests/test_console_commands.py ......                                    [ 37%]
tests/test_construction_system.py ..                                     [ 38%]
tests/test_containers.py ..                                              [ 40%]
tests/test_cook_command.py .                                             [ 40%]
tests/test_door_id_card_access.py ..                                     [ 42%]
tests/test_doors.py .                                                    [ 42%]
tests/test_environmental_protection.py .                                 [ 43%]
tests/test_equipment.py .                                                [ 44%]
tests/test_explosive_decompression.py ..                                 [ 45%]
tests/test_finance.py ...                                                [ 47%]
tests/test_fire_system.py ..                                             [ 48%]
tests/test_flood_system.py .                                             [ 49%]
tests/test_genetics.py ...                                               [ 51%]
tests/test_jobs.py ....                                                  [ 53%]
tests/test_maintenance_system.py ..                                      [ 55%]
tests/test_manifest_and_login.py ..                                      [ 56%]
tests/test_medical.py ....                                               [ 59%]
tests/test_nutrition.py .                                                [ 59%]
tests/test_pathfinding.py ..                                             [ 61%]
tests/test_performance.py .                                              [ 61%]
tests/test_performance_monitor.py .                                      [ 62%]
tests/test_persistence.py ...                                            [ 64%]
tests/test_physics.py .                                                  [ 64%]
tests/test_player_loading.py .                                           [ 65%]
tests/test_plumbing_system.py ..                                         [ 66%]
tests/test_power_system.py ..                                            [ 68%]
tests/test_random_events.py ......                                       [ 72%]
tests/test_replica_pod.py .                                              [ 72%]
tests/test_research.py ...                                               [ 74%]
tests/test_robotics.py ......                                            [ 78%]
tests/test_roles.py .........                                            [ 84%]
tests/test_room_status.py .                                              [ 85%]
tests/test_round_manager.py ..                                           [ 86%]
tests/test_security_system.py .                                          [ 87%]
tests/test_silicon.py .....                                              [ 90%]
tests/test_space_exploration.py .....                                    [ 93%]
tests/test_spatial.py ...                                                [ 95%]
tests/test_status_command.py .                                           [ 96%]
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
commands/ai.py                              42     17    60%   15-23, 30, 35-38, 41, 52, 54
commands/aliases.py                         33      9    73%   13-17, 20, 25, 37, 45
commands/antag.py                           39     20    49%   16, 24, 26, 31-49
commands/bartender.py                       15      3    80%   13, 16, 18
commands/basic.py                           26      9    65%   26-37, 56, 62
commands/botanist.py                        75     35    53%   11, 14, 23, 25, 34-42, 52, 54, 63-70, 78-86, 94, 96, 100
commands/cargo.py                           63     14    78%   15-18, 25, 30-31, 48, 51, 64, 68, 74-75, 81
commands/chef.py                            15      3    80%   13, 16, 18
commands/chemist.py                         86     21    76%   13, 16, 18, 27, 30, 32, 37, 41, 58, 61, 63, 68, 72, 74, 94, 97, 101, 104, 106, 113-114
commands/circuit.py                         25     21    16%   15-35
commands/comms.py                           34     26    24%   7-14, 19-26, 31-40
commands/consoles.py                        99     52    47%   19, 28, 31-49, 59, 63-73, 77, 80-90, 101, 105-108, 111, 114
commands/debug.py                           88     73    17%   29-51, 68-87, 103-128, 144-173, 190-219
commands/doctor.py                          67     13    81%   14, 17, 19, 23, 26, 43, 46, 56, 59, 61, 65, 68, 77
commands/engineer.py                        77     17    78%   14, 17, 27, 30, 35, 44, 53, 56, 58, 63, 72, 74, 86, 89, 93, 95, 100
commands/interaction.py                    134    110    18%   14-55, 74-86, 104-114, 130-142, 160-172, 180-194, 210-214, 230-234, 250-254, 260-287
commands/inventory.py                      149     78    48%   20, 25, 29-34, 40, 45, 52, 57-84, 91, 96-98, 104-144, 149-151, 156-158, 163, 171, 177, 182, 188, 196, 208
commands/job.py                             31     26    16%   11-43
commands/movement.py                        88     45    49%   34, 37, 44, 46, 48, 50, 52, 54, 58, 63, 70, 86, 90, 97, 126-182
commands/observation.py                    184    162    12%   31, 34-98, 113-150, 165-270, 284-339, 345-357
commands/requisition.py                     25     19    24%   10-31
commands/research.py                        25     17    32%   8-12, 18-23, 29-34
commands/security.py                        75     49    35%   14, 17, 32-42, 48-56, 62-71, 77-86, 92-94, 100-108, 114-117
commands/social.py                         109     95    13%   26-56, 71-109, 125-172, 188-237, 252-270
commands/system.py                          66     24    64%   30-39, 58-68, 85-98, 111, 116, 123, 125, 137-139, 151
components/__init__.py                      22      0   100%
components/access.py                        15      5    67%   18-26, 29
components/ai.py                            72     12    83%   60, 78, 100-101, 107, 114-119, 127, 138
components/camera.py                        18      3    83%   25-26, 29
components/circuit.py                       26      5    81%   41-44, 47
components/container.py                     90     36    60%   35, 42-43, 49, 65, 80, 84, 88-95, 99-109, 112-125, 128-140, 145, 147
components/door.py                          81     14    83%   57, 105, 127, 131, 153, 157, 169, 171, 182-186, 195
components/fluid.py                         34     11    68%   22, 24, 30, 32, 39-44, 47
components/id_card.py                        7      1    86%   14
components/item.py                         101     33    67%   54, 66-72, 85-87, 100, 104, 125-127, 148, 172, 186-208, 217
components/lathe.py                         14      7    50%   12-18
components/maintenance.py                   39      2    95%   33, 57
components/medical.py                       17      1    94%   32
components/motion_sensor.py                 14      6    57%   15-18, 21, 26
components/npc.py                           68     19    72%   41, 45, 48, 51, 54-56, 61, 63-71, 73-74, 85, 105-106, 119-121
components/player.py                       218     55    75%   91, 115, 144, 149, 152, 166, 214, 233, 237, 256, 260, 272-273, 302, 313-316, 339, 346, 349, 364-407, 417, 424, 430, 445, 474-478
components/power_consumer.py                42      1    98%   68
components/replica_pod.py                   30      4    87%   20, 23, 25, 32
components/room.py                          42     25    40%   54, 64-65, 79-83, 92-103, 112-114, 126-130, 139
components/structure.py                     42      3    93%   43, 60, 72
connection.py                               68     68     0%   6-193
engine.py                                   52     10    81%   106, 131-132, 150-151, 155-160
events.py                                   53     20    62%   89-90, 108-135, 145, 158
integration.py                             127     24    81%   64, 67, 72, 76, 80, 84, 105-106, 210-211, 217, 230-231, 242-247, 258-264, 293
mod_manager.py                              80     10    88%   47-48, 73-74, 93, 100-101, 106, 117-118
mods/example_mod/scripts/example.py          1      0   100%
mud_server.py                              194     99    49%   52-53, 98-154, 204, 233, 236-237, 239, 253-255, 309-312, 330-358, 371-394, 407-430, 444-467, 483-502, 510-519, 527-531, 548, 553-557
mud_websocket_server.py                    183    183     0%   8-406
mudpy_interface.py                         395    257    35%   249-252, 350-399, 418-422, 431, 434-435, 453, 471-568, 581-585, 597-605, 617-643, 647-666, 680, 686, 690, 705, 709, 719, 732-777, 790-860, 874-908, 921-970, 988-1022, 1053, 1065-1067, 1074, 1096-1100
parser.py                                  114     31    73%   53-54, 85-86, 104-107, 139-175, 205, 226-227, 243, 252
pathfinding.py                              29      4    86%   18, 30, 33, 46
performance.py                              43      8    81%   40, 57-64
persistence.py                             197    101    49%   19-31, 36-71, 75-112, 116-140, 146-147, 152, 182-186, 189, 193-196, 264-265, 270-272, 281-282, 293-298, 308-309
random_events.py                            35     10    71%   20-21, 23-28, 33, 46
run_server.py                               70     70     0%   8-150
script_manager.py                           77     77     0%   6-281
server.py                                  175    175     0%   6-475
settings.py                                 16     16     0%   6-41
spatial.py                                  59      3    95%   34, 64-65
start_server.py                             95     95     0%   7-192
system_loops.py                             22     22     0%   1-29
systems/__init__.py                         32      0   100%
systems/advanced_antagonists.py            111     13    88%   37, 60-67, 84-85, 97-98, 114-115, 147, 195
systems/advanced_chemistry.py               77     11    86%   37-40, 45, 78, 83, 106, 114, 132, 137
systems/ai.py                               53     13    75%   18-22, 39-40, 44, 50, 72-79
systems/antagonists.py                      53     10    81%   59, 70-77, 93
systems/atmos.py                           194     84    57%   66-67, 81-82, 90, 94, 106, 110, 116-117, 127, 129, 149-178, 188-199, 209, 215-218, 222, 226-229, 231, 235-238, 242, 246-249, 253, 256-259, 261, 264-266, 270, 328-329, 343-345, 350, 367-369, 374, 387-388, 398-401
systems/atmosphere.py                        1      0   100%
systems/bar.py                              61      4    93%   50, 53, 59, 86
systems/botany.py                          155     41    74%   65, 71, 77, 80-85, 91, 114, 117-133, 143, 150-167, 173, 187, 190
systems/cargo.py                           151     23    85%   40, 51, 96, 99, 112, 119-120, 170-175, 179-184, 218-219, 222-223
systems/chemical_reactions.py               66      4    94%   46, 52, 85, 97
systems/chemistry.py                        54      7    87%   22-23, 39, 46, 49, 56, 70
systems/circuits.py                         56     11    80%   42, 45, 56, 61-65, 69, 73, 91
systems/combat.py                           46      2    96%   48, 51
systems/communications.py                  115     30    74%   71, 79-80, 84-86, 102, 104, 106, 110-112, 117, 130, 138, 144-154, 169, 193, 204, 221-223, 232-235, 245
systems/construction.py                     97      7    93%   57, 66, 84, 93, 96, 98, 177
systems/disease.py                          64     17    73%   23, 26, 29, 35-43, 49, 52, 60, 74, 86
systems/fire.py                             47      2    96%   37, 56
systems/flood.py                            18      2    89%   20, 23
systems/gas_sim.py                         124     31    75%   98, 111-115, 120, 130, 133, 152-153, 158, 161-181
systems/genetics.py                         94      7    93%   44-45, 66, 80, 107, 111, 114
systems/hull_breach.py                      11      0   100%
systems/jobs.py                            226     21    91%   94, 151, 198, 208-209, 232-250, 282-286, 292, 313, 322-325
systems/kitchen.py                          62      4    94%   54, 57, 63, 85
systems/maintenance.py                      36      5    86%   31, 35, 38, 44, 55
systems/npc_ai.py                           31     12    61%   27, 31, 35-44
systems/physics.py                          41     12    71%   37, 40, 45, 50-58
systems/plumbing.py                         49      9    82%   29-30, 38, 45, 50, 53, 59, 63, 77
systems/power.py                           247     78    68%   66, 206-212, 230-235, 271-272, 275, 289-290, 298, 302, 319-321, 326-327, 338-345, 352, 359-361, 365-375, 378, 404-419, 453, 465-468, 479-511, 521-523, 533-542, 578
systems/random_events.py                   105     20    81%   50-52, 77-81, 86, 88, 108-109, 114, 117, 125, 137-139, 149, 161
systems/research.py                        124     18    85%   82, 85, 91, 93, 115, 117, 119, 121, 123, 132, 139-140, 153-154, 172-173, 176, 186
systems/robotics.py                        160     15    91%   72, 87, 100, 109, 115, 125, 146, 221, 229, 236, 241-245
systems/round_manager.py                    48      6    88%   33, 44, 71, 76-77, 93
systems/script_engine.py                    72     39    46%   25, 38-50, 54-57, 61, 65-71, 77-87, 96-99, 105-106, 112, 125-126, 144-151
systems/security.py                        119     25    79%   108-113, 134, 157-158, 163-164, 169-170, 183, 185-189, 201-205, 215
systems/space_exploration.py               178     16    91%   30-31, 46-47, 125, 162, 164, 174, 241, 245-248, 260, 265, 277
systems/surgery.py                          61      9    85%   35, 40, 44, 47, 50, 67, 70, 74, 102
tests/ai_tools.py                           12      0   100%
tests/test_action_queue.py                  21      0   100%
tests/test_advanced_antagonists.py          43      0   100%
tests/test_advanced_chemistry.py            16      0   100%
tests/test_ai_gameplay.py                   27      0   100%
tests/test_ai_system.py                     32      0   100%
tests/test_alias_commands.py                32      0   100%
tests/test_aliases.py                       33      0   100%
tests/test_antag_command.py                 24      0   100%
tests/test_antagonists.py                   21      0   100%
tests/test_atmos_sim.py                     25      0   100%
tests/test_bartender.py                     31      0   100%
tests/test_botany_kitchen.py                74      0   100%
tests/test_botany_mechanics.py              54      0   100%
tests/test_cargo.py                         79      0   100%
tests/test_chemical_reactions.py            34      0   100%
tests/test_chemistry.py                     75      0   100%
tests/test_circuit_system.py                30      0   100%
tests/test_cli.py                            5      0   100%
tests/test_combat_system.py                 26      0   100%
tests/test_communications.py                21      0   100%
tests/test_console_commands.py              45      0   100%
tests/test_construction_system.py           35      0   100%
tests/test_containers.py                    32      0   100%
tests/test_cook_command.py                  33      0   100%
tests/test_door_id_card_access.py           51      0   100%
tests/test_doors.py                         21      0   100%
tests/test_environmental_protection.py      15      0   100%
tests/test_equipment.py                     37      0   100%
tests/test_explosive_decompression.py       21      0   100%
tests/test_finance.py                       57      0   100%
tests/test_fire_system.py                   21      0   100%
tests/test_flood_system.py                  14      0   100%
tests/test_genetics.py                      47      0   100%
tests/test_jobs.py                          62      0   100%
tests/test_maintenance_system.py            32      0   100%
tests/test_manifest_and_login.py            52      0   100%
tests/test_medical.py                       84      0   100%
tests/test_nutrition.py                     21      0   100%
tests/test_pathfinding.py                   48      0   100%
tests/test_performance.py                   13      0   100%
tests/test_performance_monitor.py           14      0   100%
tests/test_persistence.py                   50      0   100%
tests/test_physics.py                       11      0   100%
tests/test_player_loading.py                18      0   100%
tests/test_plumbing_system.py               29      0   100%
tests/test_power_system.py                  38      0   100%
tests/test_random_events.py                 87      0   100%
tests/test_replica_pod.py                   38      0   100%
tests/test_research.py                      42      0   100%
tests/test_robotics.py                      89      0   100%
tests/test_roles.py                        104      0   100%
tests/test_room_status.py                   27      0   100%
tests/test_round_manager.py                 23      0   100%
tests/test_security_system.py               16      0   100%
tests/test_silicon.py                       56      0   100%
tests/test_space_exploration.py             77      0   100%
tests/test_spatial.py                       43      0   100%
tests/test_status_command.py                16      0   100%
tests/test_structure.py                     14      0   100%
tests/test_surgery.py                       56      0   100%
tests/test_who.py                           19      0   100%
tests/test_world_load.py                    22      0   100%
world.py                                   170     43    75%   48-49, 95, 104-110, 146-149, 153-156, 160-163, 187-188, 221, 223, 225, 227, 234, 241, 251, 304-308, 311, 322-324, 336-349
----------------------------------------------------------------------
TOTAL                                    10631   3177    70%

---------------------------------------------------- benchmark: 1 tests ----------------------------------------------------
Name (time in us)                Min       Max     Mean  StdDev   Median     IQR  Outliers  OPS (Kops/s)  Rounds  Iterations
----------------------------------------------------------------------------------------------------------------------------
test_command_performance     40.6660  529.0970  45.7950  9.9850  43.9420  3.8547   313;390       21.8365    5811           1
----------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
============================= 154 passed in 8.39s ==============================
```

### Coverage Summary
```
tests/test_who.py                           19      0   100%
tests/test_world_load.py                    22      0   100%
world.py                                   170     43    75%   48-49, 95, 104-110, 146-149, 153-156, 160-163, 187-188, 221, 223, 225, 227, 234, 241, 251, 304-308, 311, 322-324, 336-349
----------------------------------------------------------------------
TOTAL                                    10631   3177    70%

---------------------------------------------------- benchmark: 1 tests ----------------------------------------------------
Name (time in us)                Min       Max     Mean  StdDev   Median     IQR  Outliers  OPS (Kops/s)  Rounds  Iterations
----------------------------------------------------------------------------------------------------------------------------
test_command_performance     40.6660  529.0970  45.7950  9.9850  43.9420  3.8547   313;390       21.8365    5811           1
----------------------------------------------------------------------------------------------------------------------------

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

*This file was automatically generated by `generate_agents_md.sh` on 2025-06-17 05:57:32 (GitHub Actions Run #15699357258)*
