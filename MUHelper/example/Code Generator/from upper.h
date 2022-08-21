MAIN
typedef struct
{
	unsigned char ucHead0;				//1 帧头  0xAA 
	unsigned char ucHead1;				//2 帧头  0x55.0 
	unsigned char ucLength;				//3 数据长度  0x31.0 
	unsigned char ucCmd;				//4 指令   0x0E-自检;0xEE-待机;0x0D-AI_Track;0x0F-Temp_Track;0x1D-Search
	Time_Struct CurrentTime;				//5-10 时间   
	 short sFlyPAngle;				//11-12 航向角    当量：0.012
	 short sFlyYAngle;				//13-14 俯仰角    当量：0.01
	 short sFlyRAngle;				//15-16 滚转角    当量：0.01
	 int iFlyLon;				//17-20 组合经度    当量：8.381903175442434e-08
	 int iFlyLat;				//21-24 组合维度    当量：4.190951587721217e-08
	unsigned short usFlyHeight;				//25-26 卫星高度    当量：0.5
	 short sFlyTraceAngle;				//27-28 航迹角    当量：0.01
	unsigned short usFlyNSpeed;				//29-30 组合北速    当量：0.012
	unsigned short usFlyESpeed;				//31-32 组合东速    当量：0.012
	unsigned short usFlyUSpeed;				//33-34 组合天速    当量：0.012
	unsigned short usTargetDis;				//35-36 目标距离   
	 short sFyAngle;				//37-38 指定俯仰角    当量：0.01
	 short sHxAngle;				//39-40 指定方位角    当量：0.01
	 int iTargetLon;				//41-44 目标经度    当量：8.381903175442434e-08
	 int iTargetLat;				//45-48 目标维度    当量：4.190951587721217e-08
	unsigned short usTargetHeight;				//49-50 目标高度   
	unsigned char ucFrameCnt;				//51 发送帧计数   
	unsigned char ucResv;				//52 备用   
	unsigned char ucCheckSum;				//53 校验和   
}MAIN_Struct;
Time
typedef struct
{
	unsigned short usHour;				//1-2 时   
	unsigned short usMinute;				//3-4 分   
	unsigned short usSecond;				//5-6 秒   
}Time_Struct;
