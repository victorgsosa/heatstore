class Camera(object):

	def __init__(self, focal_length, height, distances = None, measures = None, roles=[]):
		self.focal_length = focal_length
		self.height = height
		self.distances = distances
		self.measures = measures
		self.roles = roles

	def has_action(self, action_id):
		actual_actions = [action.id for role in self.roles for action in role.actions]
		return action_id in actual_actions

	def has_role(self, role_id):
		return role_id in [ role.id for role in self.roles]

	def has_any_role(self, roles):
		actual_roles = [ role.id for role in self.roles]
		return any([ True for role in roles if role in actual_roles])


class Role(object):
	def __init__(self, id, description='', actions=[]):
		self.id = id
		self.description = description
		self.actions = actions


class Action(object):
	def __init__(self, id, description=''):
		self.id = id
		self.description = description
