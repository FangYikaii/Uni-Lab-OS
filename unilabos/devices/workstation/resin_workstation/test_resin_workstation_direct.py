import json
import time
import os
import sys

# 将包含unilabos的目录添加到Python路径
unilab_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
sys.path.insert(0, unilab_dir)

# 导入ResinWorkstation
from unilabos.devices.workstation.resin_workstation.resin_workstation import ResinWorkstation


def print_test_result(test_name, result):
    """
    打印测试结果
    
    Args:
        test_name: 测试名称
        result: 测试结果
    """
    status = "✓ PASS" if result else "✗ FAIL"
    print(f"{test_name:<50} {status}")
    return result


def should_continue_test(test_name):
    """
    询问用户是否继续执行特定测试
    
    Args:
        test_name: 测试名称
        
    Returns:
        bool: 用户输入YES则返回True，否则返回False
    """
    user_input = input(f"\n是否执行 {test_name}？(YES/NO): ").strip().upper()
    return user_input == "YES"


def main():
    """
    主测试函数
    
    基于新的代码逻辑（删除了任务管理功能）优化的测试脚本
    """
    print("=" * 70)
    print("ResinWorkstation 直接测试脚本")
    print("基于新逻辑优化版 - 删除了任务管理功能测试")
    print("=" * 70)
    
    # 测试配置
    address = "192.168.3.207"
    port = 8889
    
    # 创建ResinWorkstation实例
    print("\n1. 初始化测试...")
    workstation = ResinWorkstation(
        address=address,
        port=port,
        debug_mode=True
    )
    
    test_results = []
    
    # 测试初始化
    test_results.append(print_test_result("初始化ResinWorkstation", True))
    test_results.append(print_test_result("检查初始连接状态", not workstation.connected))
    test_results.append(print_test_result("检查初始操作模式", workstation.operation_mode == "local"))
        
    # 获取反应器状态
    print("\n3. 反应器状态测试...")
    if should_continue_test("获取反应器状态"):
        reactor_status = workstation._get_reactor_state(reactor_id=1)
        test_results.append(print_test_result("获取反应器状态", reactor_status is not None))
        if reactor_status:
            print(f"   反应器1温度: {reactor_status.current_temperature}°C")
            print(f"   反应器1搅拌状态: {'运行中' if reactor_status.stirring_status else '已停止'}")
    
    # 获取后处理状态
    print("\n4. 后处理状态测试...")
    if should_continue_test("获取后处理状态"):
        post_process_status = workstation._get_post_process_state(post_process_id=1)
        test_results.append(print_test_result("获取后处理状态", post_process_status is not None))
        if post_process_status:
            print(f"   后处理1状态: {post_process_status.status}")
            print(f"   后处理1清洗状态: {'清洗中' if post_process_status.cleaning_status else '未清洗'}")

    # 测试设备状态查询
    print("\n5. 设备状态测试...")
    if should_continue_test("获取设备状态"):
        status = workstation.device_status
        test_results.append(print_test_result("获取设备状态", status is not None))
        if status:
            print(f"   设备状态: {status.get('status', '未知')}")
            print(f"   连接状态: {status.get('connected', False)}")
            print(f"   操作模式: {status.get('operation_mode', '未知')}")
    
    # 测试切换本地/远程控制模式
    print("\n6. 控制模式切换测试...")
    if workstation.connected:
        if should_continue_test("切换到远程模式"):
            remote_result = workstation.toggle_local_remote_control("remote")
            test_results.append(print_test_result("切换到远程模式", remote_result))
            if remote_result:
                test_results.append(print_test_result("检查远程模式", workstation.operation_mode == "remote"))
    if workstation.connected:    
        if should_continue_test("切换回本地模式"):
            local_result = workstation.toggle_local_remote_control("local")
            test_results.append(print_test_result("切换回本地模式", local_result))
            if local_result:
                test_results.append(print_test_result("检查本地模式", workstation.operation_mode == "local"))
    
    # 测试反应器操作测试
    print("\n7. 反应器操作测试...")
    
    # 测试反应器溶液添加
    if workstation.connected: 
        if should_continue_test("反应器添加溶液"):
            solution_add_result = workstation.reactor_solution_add(
                solution_id=1,
                volume=10.0,
                reactor_id=1
            )
            test_results.append(print_test_result("反应器添加溶液", solution_add_result))
        
    # 测试氮气控制
    if workstation.connected and should_continue_test("打开氮气"):
        n2_on_result = workstation.reactor_n2_on(reactor_id=1)
        test_results.append(print_test_result("打开氮气", n2_on_result))
    
    if workstation.connected and should_continue_test("关闭氮气"):
        n2_off_result = workstation.reactor_n2_off(reactor_id=1)
        test_results.append(print_test_result("关闭氮气", n2_off_result))
    
    # 测试空气控制
    if workstation.connected and should_continue_test("打开空气"):
        air_on_result = workstation.reactor_air_on(reactor_id=1)
        test_results.append(print_test_result("打开空气", air_on_result))
    
    if workstation.connected and should_continue_test("关闭空气"):
        air_off_result = workstation.reactor_air_off(reactor_id=1)
        test_results.append(print_test_result("关闭空气", air_off_result))
    
    # 测试温度设置
    if workstation.connected and should_continue_test("设置温度"):
        temp_set_result = workstation.temp_set(reactor_id=1, temperature=25.0)
        test_results.append(print_test_result("设置温度", temp_set_result))
    
    # 测试搅拌器控制
    if workstation.connected and should_continue_test("启动搅拌器"):
        start_stir_result = workstation.start_reactor_stirrer(reactor_id=1, speed=100.0)
        test_results.append(print_test_result("启动搅拌器", start_stir_result))
    
    if workstation.connected and should_continue_test("停止搅拌器"):
        stop_stir_result = workstation.stop_reactor_stirrer(reactor_id=1)
        test_results.append(print_test_result("停止搅拌器", stop_stir_result))
    
    # 测试后处理系统
    print("\n8. 后处理系统测试...")
    
    # 后处理溶液转移
    if workstation.connected and should_continue_test("后处理溶液转移"):
        transfer_result = workstation.post_process_solution_add(
            start_bottle="bottle1",
            end_bottle="bottle2",
            volume=5.0,
            inject_speed=2.0,
            suck_speed=3.0
        )
        test_results.append(print_test_result("后处理溶液转移", transfer_result))
    
    # 后处理清洗
    if workstation.connected and should_continue_test("后处理清洗"):
        clean_result = workstation.post_process_clean(post_process_id=1)
        test_results.append(print_test_result("后处理清洗", clean_result))
    
    # 后处理排液控制
    if workstation.connected and should_continue_test("打开后处理排液"):
        discharge_on_result = workstation.post_process_discharge_on(post_process_id=1)
        test_results.append(print_test_result("打开后处理排液", discharge_on_result))
    
    if workstation.connected and should_continue_test("关闭后处理排液"):
        discharge_off_result = workstation.post_process_discharge_off(post_process_id=1)
        test_results.append(print_test_result("关闭后处理排液", discharge_off_result))
    
    # 测试等待功能
    print("\n9. 等待功能测试...")
    if workstation.connected and should_continue_test("等待1秒"):
        wait_result = workstation.wait(seconds=1)
        test_results.append(print_test_result("等待1秒", wait_result))
    
    # 测试设备断开连接
    print("\n10. 设备断开测试...")
    if workstation.connected and should_continue_test("断开设备连接"):
        disconnect_result = workstation.disconnect_device()
        test_results.append(print_test_result("断开设备连接", disconnect_result))
        if disconnect_result:
            test_results.append(print_test_result("检查断开状态", not workstation.connected))
     
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results if result)
    failed_tests = total_tests - passed_tests
    
    print(f"总测试数: {total_tests}")
    print(f"通过测试: {passed_tests}")
    print(f"失败测试: {failed_tests}")
    
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    print(f"成功率: {success_rate:.1f}%")
    
    print("\n" + "=" * 70)
    print("测试完成！")
    print("=" * 70)
    
    return passed_tests == total_tests


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)