# 🤖 Agent Development Guide

**Project:** pymud-ss13  
**Generated:** 2026-01-20 01:33:35  
**For:** New team member onboarding
**Repository:** https://github.com/yakuzadave/pymud-ss13
**Commit:** d90087a
**Branch:** main

---

## 📈 Recent Changes (Last 5 Commits)

The following commits show recent development activity. Review these to understand current work:

- **d90087a** (23 seconds ago by Katharsis): Merge pull request #192 from yakuzadave/copilot/improvement-items-review
- **da97c64** (5 days ago by copilot-swe-agent[bot]): Fix Help screen: Remove unused imports/CSS, implement visual search results display
- **6a49ebf** (7 days ago by copilot-swe-agent[bot]): Update tracking files for BATCH-005: STATUS.md, CHANGELOG.md, PROJECT_INVENTORY.md
- **4f44c4c** (7 days ago by copilot-swe-agent[bot]): Complete BATCH-005: Add search functionality to Help screen and enhance TUI screens
- **6253b28** (7 days ago by copilot-swe-agent[bot]): Update tracking files for BATCH-004: STATUS.md, CHANGELOG.md, PROJECT_INVENTORY.md

### 🔍 Detailed Recent Changes

#### Commit d90087a - Merge pull request #192 from yakuzadave/copilot/improvement-items-review
**Author:** Katharsis <34697131+yakuzadave@users.noreply.github.com>
**Date:** 2026-01-19 17:33:12
**Message:**

---
#### Commit da97c64 - Fix Help screen: Remove unused imports/CSS, implement visual search results display
**Author:** copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>
**Date:** 2026-01-15 02:39:43
**Message:**
Co-authored-by: yakuzadave <34697131+yakuzadave@users.noreply.github.com>

---
#### Commit 6a49ebf - Update tracking files for BATCH-005: STATUS.md, CHANGELOG.md, PROJECT_INVENTORY.md
**Author:** copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>
**Date:** 2026-01-13 03:01:44
**Message:**
Co-authored-by: yakuzadave <34697131+yakuzadave@users.noreply.github.com>

---

### 📁 Files Modified Recently

- CHANGELOG.md
- PROJECT_INVENTORY.md
- STATUS.md
- TASKS.md
- tui_client/screens/help.py


## 🧪 Test Results

**Status:** ✅ PASSED  
**Run Date:** 2026-01-20 01:33:45

### Test Output
```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.0.2, pluggy-1.6.0
benchmark: 5.2.3 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /home/runner/work/pymud-ss13/pymud-ss13
configfile: pytest.ini
testpaths: tests
plugins: benchmark-5.2.3, cov-7.0.0, asyncio-1.3.0, html-4.2.0, anyio-4.12.1, metadata-3.1.1
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=function, asyncio_default_test_loop_scope=function
collected 246 items

tests/test_accounts.py ...                                               [  1%]
tests/test_action_queue.py .                                             [  1%]
tests/test_advanced_antagonists.py ......                                [  4%]
tests/test_advanced_chemistry.py ..                                      [  4%]
tests/test_ai_gameplay.py .                                              [  5%]
tests/test_ai_system.py ..                                               [  6%]
tests/test_alias_commands.py ..                                          [  6%]
tests/test_aliases.py ..                                                 [  7%]
tests/test_antag_command.py .                                            [  8%]
tests/test_antagonists.py ..                                             [  8%]
tests/test_atmos_sim.py ..                                               [  9%]
tests/test_bartender.py .                                                [ 10%]
tests/test_botany_kitchen.py ....                                        [ 11%]
tests/test_botany_mechanics.py ....                                      [ 13%]
tests/test_cargo.py ..........                                           [ 17%]
tests/test_chemical_reactions.py ..                                      [ 18%]
tests/test_chemistry.py ....                                             [ 19%]
tests/test_circuit_system.py ...                                         [ 21%]
tests/test_cli.py .                                                      [ 21%]
tests/test_combat_system.py .                                            [ 21%]
tests/test_communications.py ..                                          [ 22%]
tests/test_console_commands.py ......                                    [ 25%]
tests/test_construction_system.py ..                                     [ 26%]
tests/test_containers.py ..                                              [ 26%]
tests/test_cook_command.py .                                             [ 27%]
tests/test_cyborg_med_integration.py .                                   [ 27%]
tests/test_door_id_card_access.py ..                                     [ 28%]
tests/test_doors.py .                                                    [ 28%]
tests/test_environmental_protection.py .                                 [ 29%]
tests/test_equipment.py .                                                [ 29%]
tests/test_explosive_decompression.py ..                                 [ 30%]
tests/test_finance.py ...                                                [ 31%]
tests/test_fire_system.py ..                                             [ 32%]
tests/test_flood_system.py .                                             [ 32%]
tests/test_genetic_disease_integration.py .                              [ 33%]
tests/test_genetic_med_integration.py .                                  [ 33%]
tests/test_genetics.py ...                                               [ 34%]
tests/test_inventory_sync.py .                                           [ 35%]
tests/test_item_properties.py ..                                         [ 36%]
tests/test_jobs.py .....                                                 [ 38%]
tests/test_maintenance_system.py ..                                      [ 39%]
tests/test_manifest_and_login.py ..                                      [ 39%]
tests/test_medical.py ....                                               [ 41%]
tests/test_nutrition.py .                                                [ 41%]
tests/test_pathfinding.py ..                                             [ 42%]
tests/test_performance.py .                                              [ 43%]
tests/test_performance_monitor.py .                                      [ 43%]
tests/test_persistence.py ...                                            [ 44%]
tests/test_physics.py .                                                  [ 45%]
tests/test_player_loading.py .                                           [ 45%]
tests/test_plumbing_system.py ..                                         [ 46%]
tests/test_power_system.py ..                                            [ 47%]
tests/test_random_events.py ......                                       [ 49%]
tests/test_replica_pod.py .                                              [ 50%]
tests/test_research.py ...                                               [ 51%]
tests/test_robotics.py ......                                            [ 53%]
tests/test_robotics_ai_integration.py .                                  [ 54%]
tests/test_robotics_maintenance_integration.py .                         [ 54%]
tests/test_roles.py ...........                                          [ 58%]
tests/test_room_status.py .                                              [ 59%]
tests/test_round_manager.py ..                                           [ 60%]
tests/test_security_system.py .                                          [ 60%]
tests/test_silicon.py .....                                              [ 62%]
tests/test_social_and_combat.py ....                                     [ 64%]
tests/test_space_exploration.py ......                                   [ 66%]
tests/test_spatial.py ...                                                [ 67%]
tests/test_status_command.py .                                           [ 68%]
tests/test_structure.py .                                                [ 68%]
tests/test_surgery.py ...                                                [ 69%]
tests/test_terminal_system.py ..                                         [ 70%]
tests/test_tui_client.py ............................................... [ 89%]
..                                                                       [ 90%]
tests/test_tui_logging.py ............                                   [ 95%]
tests/test_tui_playwright.py sssssssss                                   [ 99%]
tests/test_who.py .                                                      [ 99%]
tests/test_world_load.py ./home/runner/work/pymud-ss13/pymud-ss13/mud_websocket_server.py:390: SyntaxWarning: 'return' in a 'finally' block
  return websocket
                                               [100%]

=============================== warnings summary ===============================
tests/test_tui_client.py: 1005 warnings
  /home/runner/work/pymud-ss13/pymud-ss13/tui_client/client.py:153: DeprecationWarning: 'asyncio.iscoroutinefunction' is deprecated and slated for removal in Python 3.16; use inspect.iscoroutinefunction() instead
    if asyncio.iscoroutinefunction(handler):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.14.2-final-0 ________________

Name                                             Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------
account_system.py                                   46      2    96%   33, 67
action_queue.py                                     10      0   100%
cli.py                                              16     16     0%   1-21
combined_server.py                                  20     20     0%   5-40
command_spec.py                                     63     19    70%   102-125, 138, 169-173
commands/__init__.py                                 0      0   100%
commands/admin.py                                   21      1    95%   22
commands/ai.py                                      42     17    60%   15-23, 30, 35-38, 41, 52, 54
commands/aliases.py                                 33      9    73%   13-17, 20, 25, 37, 45
commands/antag.py                                   39     20    49%   16, 24, 26, 31-49
commands/bartender.py                               15      3    80%   13, 16, 18
commands/basic.py                                   26      9    65%   26-37, 56, 62
commands/botanist.py                                75     35    53%   11, 14, 23, 25, 34-42, 52, 54, 63-70, 78-86, 94, 96, 100
commands/cargo.py                                   63     14    78%   15-18, 25, 30-31, 48, 51, 64, 68, 74-75, 81
commands/chef.py                                    15      3    80%   13, 16, 18
commands/chemist.py                                 86     21    76%   13, 16, 18, 27, 30, 32, 37, 41, 58, 61, 63, 68, 72, 74, 94, 97, 101, 104, 106, 113-114
commands/circuit.py                                 25     21    16%   15-35
commands/combat.py                                  42      7    83%   20, 25, 29, 45, 50, 53, 57
commands/comms.py                                   74     58    22%   7-14, 19-26, 31-38, 43-50, 55-62, 67-76, 81-88
commands/consoles.py                                99     52    47%   19, 28, 31-49, 59, 63-73, 77, 80-90, 101, 105-108, 111, 114
commands/debug.py                                   88     73    17%   29-51, 68-87, 103-128, 144-173, 190-219
commands/doctor.py                                  67     13    81%   14, 17, 19, 23, 26, 43, 46, 56, 59, 61, 65, 68, 77
commands/engineer.py                                77     17    78%   14, 17, 27, 30, 35, 44, 53, 56, 58, 63, 72, 74, 86, 89, 93, 95, 100
commands/geneticist.py                              59     24    59%   9, 12, 20, 22, 27, 37, 41, 49-58, 63-69
commands/interaction.py                            134    110    18%   14-55, 74-86, 104-114, 130-142, 160-172, 180-194, 210-214, 230-234, 250-254, 260-287
commands/inventory.py                              149     78    48%   20, 25, 29-34, 40, 45, 52, 57-84, 91, 96-98, 104-144, 149-151, 156-158, 163, 171, 177, 182, 188, 196, 208
commands/job.py                                     31     26    16%   11-43
commands/movement.py                                88     45    49%   34, 37, 44, 46, 48, 50, 52, 54, 58, 63, 70, 86, 90, 97, 126-182
commands/observation.py                            184    162    12%   31, 34-98, 113-150, 165-270, 284-339, 345-357
commands/requisition.py                             25     19    24%   10-31
commands/research.py                                25     17    32%   8-12, 18-23, 29-34
commands/security.py                                75     49    35%   14, 17, 32-42, 48-56, 62-71, 77-86, 92-94, 100-108, 114-117
commands/social.py                                 133     99    26%   26-56, 71-109, 125-172, 188-237, 248-249, 268, 273, 288-306
commands/system.py                                  66     24    64%   30-39, 58-68, 85-98, 111, 116, 123, 125, 137-139, 151
commands/terminal.py                                11     11     0%   3-16
commands/virologist.py                              57     24    58%   9, 12, 20, 22, 26, 36, 38, 42, 50-65
components/__init__.py                              22      0   100%
components/access.py                                15      5    67%   18-26, 29
components/ai.py                                    72     12    83%   60, 78, 100-101, 107, 114-119, 127, 138
components/camera.py                                18      3    83%   25-26, 29
components/circuit.py                               26      5    81%   41-44, 47
components/container.py                             90     36    60%   35, 42-43, 49, 65, 80, 84, 88-95, 99-109, 112-125, 128-140, 145, 147
components/door.py                                  81     14    83%   57, 105, 127, 131, 153, 157, 169, 171, 182-186, 195
components/fluid.py                                 34     11    68%   22, 24, 30, 32, 39-44, 47
components/id_card.py                                7      1    86%   14
components/item.py                                 107     17    84%   54, 67, 100, 104, 125-127, 148, 172, 190, 192, 197, 199, 201-202, 207, 226
components/lathe.py                                 14      7    50%   12-18
components/maintenance.py                           39      1    97%   57
components/medical.py                               17      1    94%   32
components/motion_sensor.py                         14      6    57%   15-18, 21, 26
components/npc.py                                   68     19    72%   41, 45, 48, 51, 54-56, 61, 63-71, 73-74, 85, 105-106, 119-121
components/player.py                               227     57    75%   91, 115, 144, 149, 152, 166, 214, 233, 237, 256, 268, 280-281, 288-291, 321, 332-335, 358, 365, 368, 383-426, 436, 443, 449, 464, 495-499
components/power_consumer.py                        42      1    98%   68
components/replica_pod.py                           30      4    87%   20, 23, 25, 32
components/room.py                                  42     25    40%   54, 64-65, 79-83, 92-103, 112-114, 126-130, 139
components/structure.py                             42      3    93%   43, 60, 72
components/terminal.py                              15      3    80%   23-28
connection.py                                       68     68     0%   6-193
engine.py                                           52     10    81%   109, 134-135, 153-154, 158-163
events.py                                           53     20    62%   89-90, 108-135, 145, 158
integration.py                                     135     29    79%   64, 67, 72, 76, 80, 84, 105-106, 210-211, 217, 230-231, 243-247, 259-264, 293, 312-318
mod_manager.py                                      80     10    88%   47-48, 73-74, 93, 100-101, 106, 117-118
mods/example_mod/scripts/example.py                  1      0   100%
mud_server.py                                      243    110    55%   54-55, 100-156, 190, 193-194, 201, 204-205, 211-212, 254, 287, 290-291, 293, 299, 302-303, 332-334, 388-391, 409-437, 450-473, 486-509, 523-546, 562-581, 589-598, 606-610, 627, 632-636
mud_websocket_server.py                            187    187     0%   8-412
mudpy_interface.py                                 425    241    43%   249-252, 352-401, 420-424, 433, 436-437, 455, 473-570, 583-587, 599-607, 619-645, 649-668, 682, 688, 692, 707, 711, 732-733, 739, 756, 760, 775, 786, 789, 808-809, 815, 828-898, 912-946, 959-1008, 1026-1060, 1103-1105, 1112, 1134-1138
parser.py                                          114     31    73%   53-54, 85-86, 104-107, 139-175, 205, 226-227, 243, 252
pathfinding.py                                      29      4    86%   18, 30, 33, 46
performance.py                                      43      8    81%   40, 57-64
persistence.py                                     197    101    49%   19-31, 36-71, 75-112, 116-140, 146-147, 152, 182-186, 189, 193-196, 264-265, 270-272, 281-282, 293-298, 308-309
random_events.py                                    35     10    71%   20-21, 23-28, 33, 46
run_server.py                                       71     71     0%   8-153
script_manager.py                                   77     77     0%   6-281
server.py                                          175    175     0%   6-475
settings.py                                         16     16     0%   6-41
spatial.py                                          59      3    95%   34, 64-65
start_server.py                                     96     96     0%   7-202
system_loops.py                                     22     22     0%   1-29
systems/__init__.py                                 33      0   100%
systems/advanced_antagonists.py                    111     13    88%   37, 60-67, 84-85, 97-98, 114-115, 147, 195
systems/advanced_chemistry.py                       73     11    85%   37-40, 45, 78, 83, 106, 114, 132, 137
systems/ai.py                                       53      9    83%   18-22, 39-40, 44, 50
systems/antagonists.py                              52     10    81%   59, 70-77, 93
systems/atmos.py                                   194     84    57%   66-67, 81-82, 90, 94, 106, 110, 116-117, 127, 129, 149-178, 188-199, 209, 215-218, 222, 226-229, 231, 235-238, 242, 246-249, 253, 256-259, 261, 264-266, 270, 328-329, 343-345, 350, 367-369, 374, 387-388, 398-401
systems/atmosphere.py                                1      0   100%
systems/bar.py                                      61      4    93%   50, 53, 59, 86
systems/botany.py                                  155     41    74%   65, 71, 77, 80-85, 91, 114, 117-133, 143, 150-167, 173, 187, 190
systems/cargo.py                                   151     23    85%   40, 51, 96, 99, 112, 119-120, 170-175, 179-184, 218-219, 222-223
systems/chemical_reactions.py                       63      4    94%   46, 52, 85, 97
systems/chemistry.py                                54      7    87%   22-23, 39, 46, 49, 56, 70
systems/circuits.py                                 56     11    80%   42, 45, 56, 61-65, 69, 73, 91
systems/combat.py                                   43      2    95%   48, 51
systems/communications.py                          157     28    82%   75, 106, 110, 121, 134, 142, 148-158, 179, 191, 195, 198, 201, 214, 219, 225, 231, 268, 284-286, 295-298, 308
systems/construction.py                             97      7    93%   57, 66, 84, 93, 96, 98, 177
systems/disease.py                                  90     20    78%   27, 30, 33, 48, 51, 60, 63, 70, 77, 91, 99-100, 103, 106-112
systems/fire.py                                     46      2    96%   37, 56
systems/flood.py                                    18      2    89%   20, 23
systems/gas_sim.py                                 124     31    75%   98, 111-115, 120, 130, 133, 152-153, 158, 161-181
systems/genetics.py                                 94      7    93%   44-45, 66, 80, 107, 111, 114
systems/hull_breach.py                              11      0   100%
systems/jobs.py                                    244     21    91%   94, 151, 198, 208-209, 232-250, 282-286, 292, 313, 322-325
systems/kitchen.py                                  62      4    94%   54, 57, 63, 85
systems/maintenance.py                              36      4    89%   31, 35, 38, 44
systems/npc_ai.py                                   31     12    61%   27, 31, 35-44
systems/physics.py                                  38     12    68%   37, 40, 45, 50-58
systems/plumbing.py                                 49      9    82%   29-30, 38, 45, 50, 53, 59, 63, 77
systems/power.py                                   247     78    68%   66, 206-212, 230-235, 271-272, 275, 289-290, 298, 302, 319-321, 326-327, 338-345, 352, 359-361, 365-375, 378, 404-419, 453, 465-468, 479-511, 521-523, 533-542, 578
systems/random_events.py                           103     20    81%   50-52, 77-81, 86, 88, 108-109, 114, 117, 125, 137-139, 149, 161
systems/research.py                                124     18    85%   82, 85, 91, 93, 115, 117, 119, 121, 123, 132, 139-140, 153-154, 172-173, 176, 186
systems/robotics.py                                199     16    92%   80, 95, 118, 124, 134, 160, 237-238, 241, 254, 261, 268, 284, 290, 296, 299
systems/round_manager.py                            45      6    87%   33, 44, 71, 76-77, 93
systems/script_engine.py                            72     39    46%   25, 38-50, 54-57, 61, 65-71, 77-87, 96-99, 105-106, 112, 125-126, 144-151
systems/security.py                                107     25    77%   108-113, 134, 157-158, 163-164, 169-170, 183, 185-189, 201-205, 215
systems/space_exploration.py                       201     17    92%   31-32, 51-52, 134, 179, 181, 195, 263, 268-271, 283, 288, 309, 329
systems/surgery.py                                  61      9    85%   35, 40, 44, 47, 50, 67, 70, 74, 102
systems/terminal.py                                 37      5    86%   37, 48-51
tests/ai_tools.py                                   12      0   100%
tests/conftest.py                                   37     18    51%   25-27, 33-38, 44-50, 56, 130
tests/test_accounts.py                              26      0   100%
tests/test_action_queue.py                          21      0   100%
tests/test_advanced_antagonists.py                  43      0   100%
tests/test_advanced_chemistry.py                    16      0   100%
tests/test_ai_gameplay.py                           27      0   100%
tests/test_ai_system.py                             32      0   100%
tests/test_alias_commands.py                        32      0   100%
tests/test_aliases.py                               33      0   100%
tests/test_antag_command.py                         24      0   100%
tests/test_antagonists.py                           21      0   100%
tests/test_atmos_sim.py                             25      0   100%
tests/test_bartender.py                             31      0   100%
tests/test_botany_kitchen.py                        74      0   100%
tests/test_botany_mechanics.py                      54      0   100%
tests/test_cargo.py                                 79      0   100%
tests/test_chemical_reactions.py                    34      0   100%
tests/test_chemistry.py                             75      0   100%
tests/test_circuit_system.py                        30      0   100%
tests/test_cli.py                                    5      0   100%
tests/test_combat_system.py                         26      0   100%
tests/test_communications.py                        35      0   100%
tests/test_console_commands.py                      45      0   100%
tests/test_construction_system.py                   35      0   100%
tests/test_containers.py                            32      0   100%
tests/test_cook_command.py                          33      0   100%
tests/test_cyborg_med_integration.py                28      0   100%
tests/test_door_id_card_access.py                   51      0   100%
tests/test_doors.py                                 21      0   100%
tests/test_environmental_protection.py              15      0   100%
tests/test_equipment.py                             37      0   100%
tests/test_explosive_decompression.py               21      0   100%
tests/test_finance.py                               57      0   100%
tests/test_fire_system.py                           21      0   100%
tests/test_flood_system.py                          14      0   100%
tests/test_genetic_disease_integration.py           21      0   100%
tests/test_genetic_med_integration.py               20      0   100%
tests/test_genetics.py                              47      0   100%
tests/test_inventory_sync.py                        36      0   100%
tests/test_item_properties.py                       21      0   100%
tests/test_jobs.py                                  66      0   100%
tests/test_maintenance_system.py                    32      0   100%
tests/test_manifest_and_login.py                    61      0   100%
tests/test_medical.py                               84      0   100%
tests/test_nutrition.py                             21      0   100%
tests/test_pathfinding.py                           48      0   100%
tests/test_performance.py                           13      0   100%
tests/test_performance_monitor.py                   14      0   100%
tests/test_persistence.py                           50      0   100%
tests/test_physics.py                               11      0   100%
tests/test_player_loading.py                        18      0   100%
tests/test_plumbing_system.py                       29      0   100%
tests/test_power_system.py                          38      0   100%
tests/test_random_events.py                         87      0   100%
tests/test_replica_pod.py                           38      0   100%
tests/test_research.py                              42      0   100%
tests/test_robotics.py                              89      0   100%
tests/test_robotics_ai_integration.py               20      0   100%
tests/test_robotics_maintenance_integration.py      25      0   100%
tests/test_roles.py                                134      0   100%
tests/test_room_status.py                           27      0   100%
tests/test_round_manager.py                         23      0   100%
tests/test_security_system.py                       16      0   100%
tests/test_silicon.py                               56      0   100%
tests/test_social_and_combat.py                     62      0   100%
tests/test_space_exploration.py                     91      0   100%
tests/test_spatial.py                               43      0   100%
tests/test_status_command.py                        16      0   100%
tests/test_structure.py                             14      0   100%
tests/test_surgery.py                               56      0   100%
tests/test_terminal_system.py                       39      0   100%
tests/test_tui_client.py                           487      4    99%   345, 397, 458, 550
tests/test_tui_logging.py                          107      0   100%
tests/test_tui_playwright.py                        62     29    53%   28-42, 55-58, 74, 79, 84, 89, 103, 108, 113, 123, 128, 144-153, 167
tests/test_who.py                                   19      0   100%
tests/test_world_load.py                            22      0   100%
tui_client/__init__.py                               1      0   100%
tui_client/__main__.py                              23     23     0%   3-57
tui_client/app.py                                   64     36    44%   50-51, 55-60, 64-95, 99-101, 106-107
tui_client/client.py                               124     33    73%   100-103, 107-129, 146-147, 157-159, 172-173
tui_client/logging_config.py                        77      3    96%   152, 162-163
tui_client/screens/__init__.py                       0      0   100%
tui_client/screens/chat.py                         232    190    18%   21-24, 28-31, 218-310, 314-329, 333-335, 339-354, 358-390, 395, 411-416, 420-422, 426-428, 432-461, 469-477, 481-493, 497-511, 515-521, 525-541, 545, 549, 553-559, 563-569
tui_client/screens/game.py                         159    124    22%   125-160, 164-184, 188-189, 194-199, 203-221, 225-242, 246, 250-251, 255-259, 263-265, 269-272, 276-282, 286-301, 305-315, 326-360
tui_client/screens/help.py                          86     64    26%   147-178, 221-223, 228-259, 263-265, 269-329, 333-525, 529-672, 676-738
tui_client/screens/inventory.py                    159    121    24%   23-24, 27-33, 38-43, 47, 202-242, 247-256, 260, 264, 269-275, 279-289, 293-302, 306-310, 314-353, 357-376, 380, 384-385, 389-390, 394-395, 399-401, 405-406
tui_client/screens/login.py                         89     70    21%   87-126, 130-132, 136-143, 147-150, 154-182, 186-217, 221-230
tui_client/screens/map.py                          192    148    23%   19-26, 31-60, 230-298, 303-313, 317-318, 322, 326-332, 336-342, 346-365, 386-397, 401, 405, 409, 413, 417-418, 422-425, 429-432
world.py                                           167     43    74%   48-49, 95, 104-110, 146-149, 153-156, 160-163, 187-188, 221, 223, 225, 227, 234, 241, 251, 304-308, 311, 322-324, 336-349
------------------------------------------------------------------------------
TOTAL                                            13452   4155    69%

----------------------------------------------------- benchmark: 1 tests ----------------------------------------------------
Name (time in us)                Min       Max     Mean   StdDev   Median     IQR  Outliers  OPS (Kops/s)  Rounds  Iterations
-----------------------------------------------------------------------------------------------------------------------------
test_command_performance     32.2400  548.1640  36.6643  10.5813  34.8250  3.4460   225;326       27.2745    4846           1
-----------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
=========================== short test summary info ============================
SKIPPED [1] tests/test_tui_playwright.py:69: Requires Playwright and terminal emulator setup
SKIPPED [1] tests/test_tui_playwright.py:76: Requires Playwright and terminal emulator setup
SKIPPED [1] tests/test_tui_playwright.py:81: Requires Playwright and terminal emulator setup
SKIPPED [1] tests/test_tui_playwright.py:86: Requires Playwright and terminal emulator setup
SKIPPED [1] tests/test_tui_playwright.py:99: Requires screenshot baseline setup
SKIPPED [1] tests/test_tui_playwright.py:105: Requires screenshot baseline setup
SKIPPED [1] tests/test_tui_playwright.py:110: Requires screenshot baseline setup
SKIPPED [1] tests/test_tui_playwright.py:119: Requires performance baseline
SKIPPED [1] tests/test_tui_playwright.py:125: Requires performance baseline
================ 237 passed, 9 skipped, 1005 warnings in 6.95s =================
```

### Coverage Summary
```
tui_client/screens/login.py                         89     70    21%   87-126, 130-132, 136-143, 147-150, 154-182, 186-217, 221-230
tui_client/screens/map.py                          192    148    23%   19-26, 31-60, 230-298, 303-313, 317-318, 322, 326-332, 336-342, 346-365, 386-397, 401, 405, 409, 413, 417-418, 422-425, 429-432
world.py                                           167     43    74%   48-49, 95, 104-110, 146-149, 153-156, 160-163, 187-188, 221, 223, 225, 227, 234, 241, 251, 304-308, 311, 322-324, 336-349
------------------------------------------------------------------------------
TOTAL                                            13452   4155    69%

----------------------------------------------------- benchmark: 1 tests ----------------------------------------------------
Name (time in us)                Min       Max     Mean   StdDev   Median     IQR  Outliers  OPS (Kops/s)  Rounds  Iterations
-----------------------------------------------------------------------------------------------------------------------------
test_command_performance     32.2400  548.1640  36.6643  10.5813  34.8250  3.4460   225;326       27.2745    4846           1
-----------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
```

### Environment Info
```
Python Version: Python 3.14.2
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

*This file was automatically generated by `generate_agents_md.sh` on 2026-01-20 01:33:45 (GitHub Actions Run #21156454130)*
