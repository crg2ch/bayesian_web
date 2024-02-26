import os
import json
from flask import Blueprint, request, render_template, jsonify, make_response
from .item_manager import ItemManager

web = Blueprint('web', __name__)

current_path = os.path.abspath(__file__)
ROOT_DIR = os.path.abspath(os.path.join(current_path, "..", "..", ".."))
file_path = os.path.join(ROOT_DIR, 'src', 'data', 'youtube_data.tsv')

item_manager = ItemManager(file_path)

@web.route('/')
def index():
   item_manager.update_score()
   sorted_items = item_manager.get_sorted_items()
   return render_template('index.html', items=sorted_items)

@web.route('/detail')
def detail_page():
   impressed_video_ids_cookie = request.cookies.get('impressed_video_ids')
   video_id = request.args.get('video_id')

   item = item_manager.items[video_id]
  
   if impressed_video_ids_cookie:
       impressed_video_ids = json.loads(impressed_video_ids_cookie)
       item_manager.update_p_parameters(impressed_video_ids, video_id)
       response = make_response(render_template('detail.html', item=item, video_id=video_id))
       response.set_cookie('impressed_video_ids', '', expires=0)
   else:
       response = make_response(render_template('detail.html', item=item, video_id=video_id))
  
   return response

@web.route('/update-lambda', methods=['POST'])
def update_lambda():
   video_id = request.form['video_id']
   time_spent = float(request.form['time_spent']) / 1_000
  
   lambda_a, lambda_b = item_manager.update_lambda(video_id, time_spent)
   return f'Updated video_id: {video_id}, lambda_a: {lambda_a}, lambda_b: {lambda_b}'

@web.route('/current-state/<video_id>', methods=['GET'])
def current_state(video_id=None):
   if video_id == 'all':
      return jsonify(item_manager.show_current_state())
   return jsonify(item_manager.show_current_state(video_id))