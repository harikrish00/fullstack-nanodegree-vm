from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from database_setup import Base, MenuItem, Restaurant
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_session():
    engine = create_engine("sqlite:///restaurantmenu.db")
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind = engine)
    return DBSession()

class WebServerHandler(BaseHTTPRequestHandler):


    def do_GET(self):
        if self.path.endswith("/restaurants"):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            session = get_session()
            restaurants = session.query(Restaurant).all()
            message = ""
            message += "<html><body>Restaurants</body></html>"
            message += "<ul>"
            for r in restaurants:
                message += "<li>%s</li>" % r.name
                message += "<a href='#'>Edit</a></br>"
                message += "<a href='restaurants/%s/delete'>Delete</a></br></br>" % r.id
            message += "</ul>"
            message += "<a href='/restaurants/new'>Create New Restaurants</a>"
            message += "</body></html>"
            self.wfile.write(message)
            print message
            session.close()
            return
        elif self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            session = get_session()
            message = ""
            message += "<html><body>Create New Restaurants</body></html>"
            message += "<form method='post' action='/restaurants/new' enctype='multipart/form-data'>"
            message += "<input type='text' name='restaurant'/>"
            message += "<input type='submit' value='Submit'/>"
            message += "</form></body></html>"
            self.wfile.write(message)
            print message
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    messagecontent = fields.get('restaurant')
                session = get_session()
                restaurant = Restaurant(name = messagecontent[0])
                session.add(restaurant)
                session.commit()
                session.close()
                self.send_response(301)
                self.send_header('Content-Type','text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()
            if self.path.endswith("/delete"):
                restaurant_id = self.path.split('/')[2]
                session = get_session()
                restaurant = session.query(Restaurant).filter_by(id = int(restaurant_id)).one()
                session.delete(restaurant)
                session.commit()
                session.close()
                session.send_response(301)
                self.send_header('Content-Type','text/html')
                self.send_header('Location','/')
                self.end_headers()
        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
