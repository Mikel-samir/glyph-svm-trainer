
#class utils(object):

#    @staticmethod
def D(I , N ): 
        """ get no. of pixels to divide image with size I <tuple> to N[0]xN[1] <tuple> 
            @unsafe  : produce float no.
        """ 
        return (I[0]/N[0],I[1]/N[1])
