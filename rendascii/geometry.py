"""
TBA.
"""


import math


class Vec3D:

  def __init__(self, initializer=[0.0, 0.0, 0.0]):
    # Initialize instance attributes.
    init_type = type(initializer)
    if init_type is list:
      self.x = initializer[0]
      self.y = initializer[1]
      self.z = initializer[2]
    else:
      self.x = initializer.x
      self.y = initializer.y
      self.z = initializer.z

  def set(self, vec):
    self.x = vec.x
    self.y = vec.y
    self.z = vec.z
    return self

  def abs(self):
    self.x = -self.x if self.x < 0 else self.x
    self.y = -self.y if self.y < 0 else self.y
    self.z = -self.z if self.z < 0 else self.z
    return self

  def neg(self):
    self.x = -self.x
    self.y = -self.y
    self.z = -self.z
    return self

  def add(self, vec):
    self.x += vec.x
    self.y += vec.y
    self.z += vec.z
    return self

  def sub(self, vec):
    self.x -= vec.x
    self.y -= vec.y
    self.z -= vec.z
    return self

  def mul(self, scalar):
    self.x *= scalar
    self.y *= scalar
    self.z *= scalar
    return self

  def dot(self, vec):
    return self.x * vec.x + self.y * vec.y + self.z * vec.z

  def cross(self, vec):
    x = self.y * vec.z - self.z * vec.y
    y = self.z * vec.x - self.x * vec.z
    z = self.x * vec.y - self.y * vec.x
    self.x = x
    self.y = y
    self.z = z
    return self

  def sdist(self, vec):
    diff = self.x - vec.x
    sum = diff * diff
    diff = self.y - vec.y
    sum += diff * diff
    diff = self.z - vec.z
    sum += diff * diff
    return sum


class EulerAngles:

  def __init__(self, alpha=0, beta=0, gamma=0, order='xzy'):
    # Calculate trigonometric values.
    s1 = math.sin(alpha)
    c1 = math.cos(alpha)
    s2 = math.sin(beta)
    c2 = math.cos(beta)
    s3 = math.sin(gamma)
    c3 = math.cos(gamma)

    # Calculate rotation matrix.
    order = order.lower()
    
    if order == 'xzy':
      self.matrix = [
          Vec3D([c2 * c3, -s2, c2 * s3]),
          Vec3D([s1 * s3 + c1 * c3 * s2, c1 * c2, c1 * s2 * s3 - c3 * s1]),
          Vec3D([c3 * s1 * s2 - c1 * s3, c2 * s1, c1 * c3 + s1 * s2 * s3])
          ]

    elif order == 'xyz':
      self.matrix = [
          Vec3D([c2 * c3, -c2 * s3, s2]),
          Vec3D([c1 * s3 + c3 * s1 * s2, c1 * c3 - s1 * s2 * s3, -c2 * s1]),
          Vec3D([s1 * s3 - c1 * c3 * s2, c3 * s1 + c1 * s2 * s3, c1 * c2])
          ]

    elif order == 'yxz':
      self.matrix = [
          Vec3D([c1 * c3 + s1 * s2 * s3, c3 * s1 * s2 - c1 * s3, c2 * s1]),
          Vec3D([c2 * s3, c2 * c3, -s2]),
          Vec3D([c1 * s2 * s3 - c3 * s1, c1 * c3 * s2 + s1 * s3, c1 * c2])
          ]

    elif order == 'yzx':
      self.matrix = [
          Vec3D([c1 * c2, s1 * s3 - c1 * c3 * s2, c3 * s1 + c1 * s2 * s3]),
          Vec3D([s2, c2 * c3, -c2 * s3]),
          Vec3D([-c2 * s1, c1 * s3 + c3 * s1 * s2, c1 * c3 - s1 * s2 * s3])
          ]

    elif order == 'zyx':
      self.matrix = [
          Vec3D([c1 * c2, c1 * s2 * s3 - c3 * s1, s1 * s2 + c1 * c3 * s2]),
          Vec3D([c2 * s1, c1 * c3 + s1 * s2 * s3, c3 * s1 * s2 - c1 * s3]),
          Vec3D([-s2, c2 * s3, c2 * c3])
          ]

    elif order == 'zxy':
      self.matrix = [
          Vec3D([c1 * c3 - s1 * s2 * s3, -c2 * s1, c1 * s3 + c3 * s1 * s2]),
          Vec3D([c3 * s1 + c1 * s2 * s3, c1 * c2, s1 * s3 - c1 * c3 * s2]),
          Vec3D([-c2 * s3, s2, c2 * c3])
          ]

  def transform(self, vec):
    x = self.matrix[0].dot(vec)
    y = self.matrix[1].dot(vec)
    z = self.matrix[2].dot(vec)
    vec.x = x
    vec.y = y
    vec.z = z


class Polygon:

  def __init__(self, vertices, normal):
    # Initialize instance attributes.
    self.vertices = vertices
    self.normal = normal
    self.proj_bound_min = Vec2D([None, None])
    self.proj_bound_max = Vec2D([None, None])

  def update_bounds_2d(self):
    # Calculate 2D AABB.
    for vertex in self.vertices:
      if self.proj_bound_min.x is None or vertex.x < self.proj_bound_min.x:
        self.proj_bound_min.x = vertex.x
      if self.proj_bound_min.y is None or vertex.y < self.proj_bound_min.y:
        self.proj_bound_min.y = vertex.y
      if self.proj_bound_max.x is None or vertex.x > self.proj_bound_max.x:
        self.proj_bound_max.x = vertex.x
      if self.proj_bound_max.y is None or vertex.y > self.proj_bound_max.y:
        self.proj_bound_max.y = vertex.y

  def interpolate_z(self, vec):
    # Calculate baycentric weights.
    area_t = self._triangle_area_2d(*self.vertices)
    w0 = self._triangle_area_2d(vec, vertices[1], vertices[2]) / area_t
    w1 = self._triangle_area_2d(vec, vertices[2], vertices[0]) / area_t
    w2 = self._triangle_area_2d(vec, vertices[0], vertices[1]) / area_t

    return (
        w0 * self.vertices[0].z
        + w1 * self.vertices[1].z
        + w2 * self.vertices[2].z
        )

  def contains_point_2d(self, vec):
    # Check if vector is inside AABB.
    if (
        self.proj_bound_min.x < vec.x < self.proj_bound_max.x
        and self.proj_bound_min.y < vec.y < self.proj_bound_max.y
        ):
      # Check if vector is inside polygon.
      start = self._edge_2d(vec, self.vertices[-1], self.vertices[0]) < 0

      for i in range(len(self.vertices) - 1):
        if (
            (self._edge_2d(vec, self.vertices[i], self.vertices[i + 1]) <= 0)
            != start
            ):
          return False

      return True

    return False

  def _edge_2d(self, vec, line_s, line_e):
    # Check which side of line a vector lies on (sign).
    return (
        (vec.x - line_e.x) * (line_s.y - line_e.y)
        - (line_s.x - line_e.x) * (vec.y - line_e.y)
        )

  def _triangle_area_2d(self, v0, v1, v2):
    return 0.5 * math.abs(
        v0.x * v1.y+ v1.x * v2.y + v2.x * v0.y
        - v0.x * v2.y - v2.x * v1.y - v1.x * v0.y
        )
