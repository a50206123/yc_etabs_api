from etabs import ETABS

etabs = ETABS()

############  POINTS  ############
def test_point_add() :
    ret = etabs.Points.add([100, 100, 40.35])
    print(ret) # Return unique of adding point
def test_point_delete(unique : str) :
    ret = etabs.Points.delete(unique)
    print(ret) # Return None
def test_point_get_name_list(by_unique = True) :
    ret = etabs.Points.get_name_list(by_unique)
    print(ret)
    # by_unique = True --> Return list of unique
    # by_unique = False --> Return list of label
def test_point_set_suppot(unique:str, UX = False, UY = False, UZ = False,
                   RX = False, RY = False, RZ = False, quick:str = None) :
    ret = etabs.Points.set_suppot(unique, UX, UY, UZ, RX, RY, RZ, quick)
    print(ret)

if __name__ == '__main__' :
    # test_point_add() # OK, Add a point at (100, 100, 40.35)
    # test_point_delete('24') # OK, Delete point 24

    # test_point_get_name_list(by_unique=True) # OK, Get Name List by unique
    # test_point_get_name_list(by_unique=False) # OK, Get Name List by label

    test_point_set_suppot('293', quick='pin') # Set point to pin
    test_point_set_suppot('183', quick='free') # Set point to free
    test_point_set_suppot('294', quick='roller') # Set point to roller
    test_point_set_suppot('190', quick='fix') # Set point to fix
    pass
