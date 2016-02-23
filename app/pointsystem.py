
import pickledb

class PointsSystem():
    db = pickledb.load('points.db', False)
    def points(self, action, points):
        points = int(points)
        currentpoints =  self.db.get('points') or 0
        if( action == 'Add'):
            currentpoints += points
        elif (action == 'Remove'):
            currentpoints -= points
        self.db.set('points', currentpoints)
        self.db.dump()
        return str(currentpoints)
    
    def getpoints(self):
        currentpoints =  self.db.get('points')
        return str(currentpoints)

