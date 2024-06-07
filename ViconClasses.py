from vicon_dssdk import ViconDataStream

class MAS:

    vicon_server_ip = 'l-hvhnpt3'
    #vicon_server_ip = '192.168.68.52'
    vicon_server_port = '801'

    def __init__(self):
        self.log = open("viconLog.txt", 'w')
        self.vicon_client = ViconDataStream.Client()

        try:
            print("Connecting to Vicon server ...")
            self.vicon_client.Connect(f"{self.vicon_server_ip}:{self.vicon_server_port}")
            self.vicon_client.SetBufferSize(3)
            self.vicon_client.EnableSegmentData()

            has_frame = False

            while not has_frame:
                self.vicon_client.GetFrame()
                has_frame = True

        except ViconDataStream.DataStreamException as e:
            print('Vicon Datastream Error: ', e)


    def log_data(self, data):
        self.log.write(data)

    def get_client(self):
        return self.vicon_client

class Location:
    def __init__(self, toy, mas,subject_ind):
        self.mas = mas
        self.toy = toy 
        self.subject_ind = subject_ind
        self.WAYPOINT_RANGE = 50
    def getPosition(self):
        self.mas.vicon_client.GetFrame()
        client = self.mas.vicon_client
        subject_names = client.GetSubjectNames()
        segment_names = client.GetSegmentNames(subject_name[subject_ind])
        global_position = client.GetSegmentGlobalTranslation(subject_name[subject_ind], segment_name[subject_ind])
        global_orientation = client.GetSegmentGlobalRotationEulerXYZ(subject_name[subject_ind], segment_name[subject_ind])
        xVicon = global_position[0][0]/10
        yVicon = global_position[0][1]/10
        data = str(segment_names) + " , " + str(xVicon) + ", " + str(yVicon) + ", " + str(xSphero) + ", " + str(ySphero)
        self.mas.log_data(data+"\n")
        xvic, yvic, zvic = global_position[0]
        rollvic, pitchvic, yawvic = global_orientation[0]
        return xVicon , yVicon