#!flask/bin/python
from flask import Flask, jsonify
from flask import make_response
from flask import request
import OptimalRoute

app = Flask(__name__)


addresses = [
    {
        'id': 1,
        'address': u"55+Hamilton+Drive+Baltimore+MD"
    },
        {
        'id': 2,
        'address': u"4601+Cambridge+Place+Baltimore+MD"
    },
        {
        'id': 3,
        'address': u"2032+Hamilton+Drive+Baltimore+MD"
    },
        {
        'id': 4,
        'address': u"3226+Marshall+Street+Baltimore+MD"
    },
        {
        'id': 5,
        'address': u"1057+Cambridge+Place+Baltimore+MD"
    },
        {
        'id': 6,
        'address': u"1104+Hamilton+Drive+Baltimore+MD"
    },
        {
        'id': 7,
        'address': u"3883+Calvin+Street+Baltimore+MD"
    },
        {
        'id': 8,
        'address': u"200+Ridgewood+Road+Baltimore+MD"
    },
            {
        'id': 8,
        'address': u"624+Gutman+Ave+Baltimore+MD"
    },
            {
        'id': 8,
        'address': u"600+North+Charles+Street+Baltimore+MD"
    },
            {
        'id': 8,
        'address': u"3134+Eastern+Ave+Baltimore+MD"
    },
            {
        'id': 8,
        'address': u"1601+Eeast+North+Avenue+Baltimore+MD"
    },
            {
        'id': 8,
        'address': u"2401+Liberty+Heights+Ave+Baltimore+MD"
    },
            {
        'id': 8,
        'address': u"2413+Frederick+Avenue+Baltimore+MD"
    },
            {
        'id': 8,
        'address': u"3559+Boston+Street+Baltimore+MD"
    },
]

routes = None

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/addresses', methods=['GET'])
def get_addresses():
    return jsonify({'addresses': addresses})

@app.route('/addresses/<int:address_id>', methods=['GET'])
def get_address(address_id):
    address = [address for address in addresses if address['id'] == address_id]
    if len(address) == 0:
        abort(404)
    return jsonify({'address': address[0]})


@app.route('/addresses', methods=['POST'])
def create_address():
    if not request.json or not 'address' in request.json:
        abort(400)
    address = {
        'id': addresses[-1]['id'] + 1,
        'address': request.json['address'],
    }
    addresses.append(address)
    A = jsonify({'address': address})
    return make_response(A)

@app.route('/routes',methods = ['GET'])
def get_routes():
  return make_response(jsonify(routes))

@app.route('/routes/<int:route_id>',methods = ['GET'])
def get_route(route_id):
    routes_ = [route for route in routes if route['id'] == route_id]
    if len(routes_) == 0:
        abort(404)
    return make_response(jsonify(routes_[0]))



@app.route('/make_routes',methods=['POST'])
def make_routes():
      global routes
      if not request.json or not 'no_cars' in request.json:
        abort(400)

      no_cars = request.json['no_cars']
      l_addresses = [el["address"] for el in addresses]
      result_indices = OptimalRoute.get_optimal_route(l_addresses, depot = 0, num_vehicles = no_cars)
      #result_indices = OptimalRoute.get_optimal_route(None, depot = 0, num_vehicles = no_cars)
      routes = [{"route":[addresses[dest]["address"] for dest in route],"id":r_id} for r_id, route in enumerate(result_indices)]

      for r in routes:
          r["url"] = OptimalRoute.google_maps_string(r["route"])
      return make_response(jsonify(routes))
      
if __name__ == '__main__':
    app.run(debug=True)