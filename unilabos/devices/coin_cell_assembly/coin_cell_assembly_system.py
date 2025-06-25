import json
from pymodbus.client import ModbusTcpClient
from unilabos.device_comms.modbus_plc.node.modbus import WorderOrder, Coil, DiscreteInputs, HoldRegister, InputRegister, DataType
from pymodbus.constants import Endian
import time
from typing import Callable
from unilabos.device_comms.modbus_plc.client import TCPClient, ModbusNode, PLCWorkflow, ModbusWorkflow, WorkflowAction, BaseClient
from unilabos.device_comms.modbus_plc.node.modbus import DeviceType, Base as ModbusNodeBase, DataType, WorderOrder


class Coin_Cell_Assembly:
    """
    This provides a python class for the YIHUA COIN CELL ASSEMBLY SYSTEM. It provides functions to read and write to the system.
    """
    def __init__(self, address=None, port=None):
        """
        Initializer of the Coin_Cell_Assembly class.
        This function sets up the modbus tcp connection to the YIHUA COIN CELL ASSEMBLY SYSTEM
        """
        modbus_client = TCPClient(addr=address, port=port)
        self.nodes = BaseClient.load_csv('./coil_cell_assembly.csv')
        self.client  = modbus_client.register_node_list(self.nodes)
        self.success = False

    # ====================== 命令类指令（COIL_x_） ======================

    def sys_start_cmd(self, cmd):
        """设备启动命令 (可读写)"""
        if cmd is not None:  # 写入模式
            self.success = False
            node = self.client.use_node('COIL_SYS_START_CMD')
            node.write(cmd)
            self.success = True
            return self.success
        else:  # 读取模式
            cmd_feedback, read_err =  self.client.use_node('COIL_SYS_STOP_CMD').read(1)
            return cmd_feedback[0]

    def sys_stop_cmd(self, cmd=None):
        """设备停止命令 (可读写)"""
        if cmd is not None:  # 写入模式
            self.success = False
            node = self.client.use_node('COIL_SYS_STOP_CMD')
            node.write(cmd)
            self.success = True
            return self.success
        else:  # 读取模式
            cmd_feedback, read_err = self.client.use_node('COIL_SYS_STOP_CMD').read(1)
            return cmd_feedback[0]

    def sys_reset_cmd(self, cmd=None):
        """设备复位命令 (可读写)"""
        if cmd is not None:
            self.success = False
            self.client.use_node('COIL_SYS_RESET_CMD').write(cmd)
            self.success = True
            return self.success
        else:
            cmd_feedback, read_err = self.client.use_node('COIL_SYS_RESET_CMD').read(1)
            return cmd_feedback[0]

    def sys_hand_cmd(self, cmd=None):
        """手动模式命令 (可读写)"""
        if cmd is not None:
            self.success = False
            self.client.use_node('COIL_SYS_HAND_CMD').write(cmd)
            self.success = True
            return self.success
        else:
            cmd_feedback, read_err = self.client.use_node('COIL_SYS_HAND_CMD').read(1)
            return cmd_feedback[0]

    def sys_auto_cmd(self, cmd=None):
        """自动模式命令 (可读写)"""
        if cmd is not None:
            self.success = False
            self.client.use_node('COIL_SYS_AUTO_CMD').write(cmd)
            self.success = True
            return self.success
        else:
            cmd_feedback, read_err = self.client.use_node('COIL_SYS_AUTO_CMD').read(1)
            return cmd_feedback[0]

    def sys_init_cmd(self, cmd=None):
        """初始化命令 (可读写)"""
        if cmd is not None:
            self.success = False
            self.client.use_node('COIL_SYS_INIT_CMD').write(cmd)
            self.success = True
            return self.success
        else:
            cmd_feedback, read_err = self.client.use_node('COIL_SYS_INIT_CMD').read(1)
            return cmd_feedback[0]

    def unilab_send_msg_succ_cmd(self, cmd=None):
        """UNILAB发送配方完毕 (可读写)"""
        if cmd is not None:
            self.success = False
            self.client.use_node('COIL_UNILAB_SEND_MSG_SUCC_CMD').write(cmd)
            self.success = True
            return self.success
        else:
            cmd_feedback, read_err = self.client.use_node('COIL_UNILAB_SEND_MSG_SUCC_CMD').read(1)
            return cmd_feedback[0]

    def unilab_rec_msg_succ_cmd(self, cmd=None):
        """UNILAB接收测试户籍完毕 (可读写)"""
        if cmd is not None:
            self.success = False
            self.client.use_node('COIL_UNILAB_REC_MSG_SUCC_CMD').write(cmd)
            self.success = True
            return self.success
        else:
            cmd_feedback, read_err = self.client.use_node('COIL_UNILAB_REC_MSG_SUCC_CMD').read(1)
            return cmd_feedback

  # ====================== 命令类指令（REG_x_） ======================
    def unilab_send_msg_electrolyte_num(self, num=None):
        """UNILAB写电解液使用瓶数(可读写)"""
        if num is not None:
            self.success = False
            self.client.use_node('REG_MSG_ELECTROLYTE_NUM').write(num)
            self.success = True
            return self.success
        else:
            cmd_feedback, read_err = self.client.use_node('REG_MSG_ELECTROLYTE_NUM').read(1)
            return cmd_feedback[0]

    def unilab_send_msg_electrolyte_use_num(self, use_num):
        """UNILAB写电解液使用瓶数(可读写)"""
        if use_num is not None:
            self.success = False
            self.client.use_node('REG_MSG_ELECTROLYTE_USE_NUM').write(use_num)
            self.success = True
            return self.success
        else:
            return False

    def unilab_send_msg_assembly_type(self, num=None):
        """UNILAB写组装参数"""
        if num is not None:
            self.success = False
            self.client.use_node('REG_MSG_ASSEMBLY_TYPE').write(num)
            self.success = True
            return self.success
        else:
            cmd_feedback, read_err = self.client.use_node('REG_MSG_ASSEMBLY_TYPE').read(1)
            return cmd_feedback[0]

    def unilab_send_msg_electrolyte_vol(self, vol=None):
        """UNILAB写电解液吸取量参数"""
        if vol is not None:
            self.success = False
            self.client.use_node('REG_MSG_ELECTROLYTE_VOLUME').write(vol, data_type=DataType.FLOAT32, word_order=WorderOrder.LITTLE)
            self.success = True
            return self.success
        else:
            cmd_feedback, read_err = self.client.use_node('REG_MSG_ELECTROLYTE_VOLUME').read(2, word_order=WorderOrder.LITTLE)
            return cmd_feedback[0]

    def unilab_send_msg_cmd(self, experiment_params=None):
        """UNILAB写参数"""
        if self.request_rec_msg_status:
            if experiment_params is not None:
                self.success = False
                data = json.loads(experiment_params)
                self.unilab_send_msg_electrolyte_num(data['elec_num'])
                time.sleep(1)
                self.unilab_send_msg_electrolyte_use_num(data['elec_use_num'])
                time.sleep(1)
                self.unilab_send_msg_assembly_type(data['assembly_type'])
                self.unilab_send_msg_succ_cmd(True)
                self.success = True
                return self.success
            else:
                return False
        else:
            return False

    # ==================== 状态类属性（COIL_x_STATUS） ====================
    @property
    def sys_start_status(self) -> bool:
        """设备启动中( BOOL)"""
        status, read_err = self.client.use_node('COIL_SYS_START_STATUS').read(1)
        return status[0]

    @property
    def sys_stop_status(self) -> bool:
        """设备停止中( BOOL)"""
        status, read_err = self.client.use_node('COIL_SYS_STOP_STATUS').read(1)
        return status[0]

    @property
    def sys_reset_status(self) -> bool:
        """设备复位中( BOOL)"""
        status, read_err = self.client.use_node('COIL_SYS_RESET_STATUS').read(1)
        return status[0]

    @property
    def sys_hand_status(self) -> bool:
        """设备手动模式( BOOL)"""
        status, read_err = self.client.use_node('COIL_SYS_HAND_STATUS').read(1)
        return status[0]

    @property
    def sys_auto_status(self) -> bool:
        """设备自动模式( BOOL)"""
        status, read_err = self.client.use_node('COIL_SYS_AUTO_STATUS').read(1)
        return status[0]

    @property
    def sys_init_status(self) -> bool:
        """设备初始化完成( BOOL)"""
        status, read_err = self.client.use_node('COIL_SYS_INIT_STATUS').read(1)
        return status[0]

    @property
    def request_rec_msg_status(self) -> bool:
        """设备请求接受配方( BOOL)"""
        status, read_err = self.client.use_node('COIL_REQUEST_REC_MSG_STATUS').read(1)
        return status[0]

    @property
    def request_send_msg_status(self) -> bool:
        """设备请求发送测试数据( BOOL)"""
        status, read_err = self.client.use_node('COIL_REQUEST_SEND_MSG_STATUS').read(1)
        return status[0]

    # ======================= 其他属性（特殊功能） ========================
    '''
    @property
    def warning_1(self) -> bool:
        status, read_err = self.client.use_node('COIL_WARNING_1').read(1)
        return status[0]
    '''
    # ===================== 生产数据区 ======================
    
    @property
    def data_assembly_coin_cell_num(self) -> int:
        """已完成电池数量 (INT16)"""
        num, read_err = self.client.use_node('REG_DATA_ASSEMBLY_COIN_CELL_NUM').read(1)
        return num

    @property
    def data_open_circuit_voltage(self) -> float:
        """开路电压值 (FLOAT32)"""
        vol, read_err =  self.client.use_node('REG_DATA_OPEN_CIRCUIT_VOLTAGE').read(2, word_order=WorderOrder.LITTLE)
        return vol

    @property
    def data_axis_x_pos(self) -> float:
        """分液X轴当前位置 (FLOAT32)"""
        pos, read_err =  self.client.use_node('REG_DATA_AXIS_X_POS').read(2, word_order=WorderOrder.LITTLE)
        return pos

    @property
    def data_axis_y_pos(self) -> float:
        """分液Y轴当前位置 (FLOAT32)"""
        pos, read_err =  self.client.use_node('REG_DATA_AXIS_Y_POS').read(2, word_order=WorderOrder.LITTLE)
        return pos

    @property
    def data_axis_z_pos(self) -> float:
        """分液Z轴当前位置 (FLOAT32)"""
        pos, read_err =  self.client.use_node('REG_DATA_AXIS_Z_POS').read(2, word_order=WorderOrder.LITTLE)
        return pos

    @property
    def data_pole_weight(self) -> float:
        """当前电池正极片称重数据 (FLOAT32)"""
        weight, read_err =  self.client.use_node('REG_DATA_POLE_WEIGHT').read(2, word_order=WorderOrder.LITTLE)
        return weight

    @property
    def data_coin_cell_code(self) -> str:
        """电池二维码序列号 (INT16)"""
        code, read_err =  self.client.use_node('REG_DATA_COIN_CELL_CODE').read(10, word_order=WorderOrder.LITTLE)
        clean_code = code.strip('\x00')
        reversed_code = clean_code[::-1]
        return reversed_code


    @property
    def data_electrolyte_code(self) -> str:
        """电解液二维码序列号 (INT16)"""
        code, read_err =  self.client.use_node('REG_DATA_ELECTROLYTE_CODE').read(10, word_order=WorderOrder.LITTLE)
        clean_code = code.strip('\x00')
        reversed_code = clean_code[::-1]
        return reversed_code

    # ===================== 环境监控区 ======================
    @property
    def data_glove_box_pressure(self) -> float:
        """手套箱压力 (bar, FLOAT32)"""
        status, read_err = self.client.use_node('REG_DATA_GLOVE_BOX_PRESSURE').read(2, word_order=WorderOrder.LITTLE)
        return status

    @property
    def data_glove_box_o2_content(self) -> float:
        """手套箱氧含量 (ppm, FLOAT32)"""
        value, read_err = self.client.use_node('REG_DATA_GLOVE_BOX_O2_CONTENT').read(2, word_order=WorderOrder.LITTLE)
        return value

    @property
    def data_glove_box_water_content(self) -> float:
        """手套箱水含量 (ppm, FLOAT32)"""
        value, read_err = self.client.use_node('REG_DATA_GLOVE_BOX_WATER_CONTENT').read(2, word_order=WorderOrder.LITTLE)
        return value

    '''
    @property
    def data_stack_vision_code(self) -> int:
        """物料堆叠复检图片编码 (INT16)"""
        code, read_err =  self.client.use_node('REG_DATA_STACK_VISON_CODE').read(1)
        return code

    @property
    def data_assembly_time(self) -> int:
        """单颗电池组装时间 (秒, INT16)"""
        time, read_err =  self.client.use_node('REG_DATA_ASSEMBLY_TIME').read(1)
        return time


    # ===================== 物料管理区 ======================
    @property
    def data_material_inventory(self) -> int:
        """主物料库存 (数量, INT16)"""
        inventory, read_err =  self.client.use_node('REG_DATA_MATERIAL_INVENTORY').read(1)
        return inventory

    @property
    def data_tips_inventory(self) -> int:
        """移液枪头库存 (数量, INT16)"""
        inventory, read_err = self.client.register_node_list(self.nodes).use_node('REG_DATA_TIPS_INVENTORY').read(1)
        return inventory
        
    '''

if __name__ == '__main__':
    coin_cell_assmbly = Coin_Cell_Assembly(address="192.168.1.20", port="502")
    while True:
        # cmd coil
        print('start cmd:', coin_cell_assmbly.sys_start_cmd(True))
        time.sleep(1)
        print('stop cmd:', coin_cell_assmbly.sys_stop_cmd(False))
        time.sleep(1)
        print('reset cmd:', coin_cell_assmbly.sys_reset_cmd(True))
        time.sleep(1)
        print('hand cmd:', coin_cell_assmbly.sys_hand_cmd(False))
        time.sleep(1)
        print('auto cmd:', coin_cell_assmbly.sys_auto_cmd(True))
        time.sleep(1)
        print('init cmd:', coin_cell_assmbly.sys_init_cmd(False))
        time.sleep(1)
        print('send msg succ cmd:', coin_cell_assmbly.unilab_send_msg_succ_cmd(False))
        time.sleep(1)
        print('rec msg succ cmd:', coin_cell_assmbly.unilab_rec_msg_succ_cmd(True))
        time.sleep(1)

        # cmd reg
        print('elec use num msg:', coin_cell_assmbly.unilab_send_msg_electrolyte_use_num(8))
        time.sleep(1)
        print('elec num msg:', coin_cell_assmbly.unilab_send_msg_electrolyte_num(4))
        time.sleep(1)
        print('elec vol msg:', coin_cell_assmbly.unilab_send_msg_electrolyte_vol(3.3))
        time.sleep(1)
        print('assembly type msg:', coin_cell_assmbly.unilab_send_msg_assembly_type(1))
        time.sleep(1)   

        # status coil
        print('start status:',coin_cell_assmbly.sys_start_status)
        time.sleep(1)
        print('stop status:',coin_cell_assmbly.sys_stop_status)
        time.sleep(1)
        print('reset status:',coin_cell_assmbly.sys_reset_status)
        time.sleep(1)
        print('hand status:',coin_cell_assmbly.sys_hand_status)
        time.sleep(1)
        print('auto status:', coin_cell_assmbly.sys_auto_status)
        time.sleep(1)
        print('init ok:', coin_cell_assmbly.sys_init_status)
        time.sleep(1)
        print('request rec msg:', coin_cell_assmbly.request_rec_msg_status)
        time.sleep(1)
        print('request send msg:', coin_cell_assmbly.request_send_msg_status)
        time.sleep(1)

        # status reg
        print('assembly coin cell num:', coin_cell_assmbly.data_assembly_coin_cell_num)
        time.sleep(1)
        print('open circuit vol:', coin_cell_assmbly.data_open_circuit_voltage)
        time.sleep(1)
        print('axis x pos:', coin_cell_assmbly.data_axis_x_pos)
        time.sleep(1)
        print('axis y pos:', coin_cell_assmbly.data_axis_y_pos)
        time.sleep(1)
        print('axis z pos:', coin_cell_assmbly.data_axis_z_pos)
        time.sleep(1)
        print('pole weight:', coin_cell_assmbly.data_pole_weight)
        time.sleep(1)
        print('coin cell code:', coin_cell_assmbly.data_coin_cell_code)
        time.sleep(1)
        print('elec code:', coin_cell_assmbly.data_electrolyte_code)
        time.sleep(1)
        print('glove box pressure:', coin_cell_assmbly.data_glove_box_pressure)
        time.sleep(1)
        print('glove box o2:', coin_cell_assmbly.data_glove_box_o2_content)
        time.sleep(1)
        print('glove box water:', coin_cell_assmbly.data_glove_box_water_content)
        time.sleep(1)

