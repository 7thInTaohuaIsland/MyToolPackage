MAIN
typedef struct
{
	unsigned char ucHead0;				//1 ֡ͷ  0xAA 
	unsigned char ucHead1;				//2 ֡ͷ  0x55.0 
	unsigned char ucLength;				//3 ���ݳ���  0x31.0 
	unsigned char ucCmd;				//4 ָ��   0x0E-�Լ�;0xEE-����;0x0D-AI_Track;0x0F-Temp_Track;0x1D-Search
	Time_Struct CurrentTime;				//5-10 ʱ��   
	 short sFlyPAngle;				//11-12 �����    ������0.012
	 short sFlyYAngle;				//13-14 ������    ������0.01
	 short sFlyRAngle;				//15-16 ��ת��    ������0.01
	 int iFlyLon;				//17-20 ��Ͼ���    ������8.381903175442434e-08
	 int iFlyLat;				//21-24 ���ά��    ������4.190951587721217e-08
	unsigned short usFlyHeight;				//25-26 ���Ǹ߶�    ������0.5
	 short sFlyTraceAngle;				//27-28 ������    ������0.01
	unsigned short usFlyNSpeed;				//29-30 ��ϱ���    ������0.012
	unsigned short usFlyESpeed;				//31-32 ��϶���    ������0.012
	unsigned short usFlyUSpeed;				//33-34 �������    ������0.012
	unsigned short usTargetDis;				//35-36 Ŀ�����   
	 short sFyAngle;				//37-38 ָ��������    ������0.01
	 short sHxAngle;				//39-40 ָ����λ��    ������0.01
	 int iTargetLon;				//41-44 Ŀ�꾭��    ������8.381903175442434e-08
	 int iTargetLat;				//45-48 Ŀ��ά��    ������4.190951587721217e-08
	unsigned short usTargetHeight;				//49-50 Ŀ��߶�   
	unsigned char ucFrameCnt;				//51 ����֡����   
	unsigned char ucResv;				//52 ����   
	unsigned char ucCheckSum;				//53 У���   
}MAIN_Struct;
Time
typedef struct
{
	unsigned short usHour;				//1-2 ʱ   
	unsigned short usMinute;				//3-4 ��   
	unsigned short usSecond;				//5-6 ��   
}Time_Struct;
