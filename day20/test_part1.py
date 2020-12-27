import unittest

import numpy.testing

from part1 import *

class TestPart1(unittest.TestCase):
    def test_load_tiles(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_id = 2311

        self.assertEqual(len(tiles), 9)

        self.assertIn(tile_id, tiles)

        expected_arr = np.array([
            list('..##.#..#.'),
            list('##..#.....'),
            list('#...##..#.'),
            list('####.#...#'),
            list('##.##.###.'),
            list('##...#.###'),
            list('.#.#.#..##'),
            list('..#....#..'),
            list('###...#.#.'),
            list('..###..###'),
        ])

        self.assertEqual(tiles[tile_id].shape, expected_arr.shape)
        numpy.testing.assert_equal(
            expected_arr,
            tiles[tile_id]
        )

    def test_edges(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)
        
        tile_id = 2311
        self.assertIn(tile_id, tile_map)

        edges = tile_map[tile_id]['edges']
        expected_edges = np.array([
            list('..##.#..#.'), # Top
            list('..###..###'), # Bottom
            list('.#####..#.'), # Left
            list('...#.##..#'), # Right
        ])

        self.assertEqual(edges.shape, expected_edges.shape)

        numpy.testing.assert_equal(
            edges,
            expected_edges
        )

    def test_rotate_1(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)
        
        tile_id = 2311
        self.assertIn(tile_id, tile_map)

        edges = tile_map[tile_id]['edges']

        expected_edges_1 = np.array([
            list('...#.##..#'), # Top
            list('.#####..#.'), # Bottom
            list('.#..#.##..'), # Left
            list('###..###..'), # Right
        ])
        r1_edges = rotate(edges, 1)
        numpy.testing.assert_equal(r1_edges, expected_edges_1)
    
    def test_rotate_2(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)
        
        tile_id = 2311
        self.assertIn(tile_id, tile_map)

        edges = tile_map[tile_id]['edges']

        expected_edges_2 = np.array([
            list('###..###..'), # Top
            list('.#..#.##..'), # Bottom
            list('#..##.#...'), # Left
            list('.#..#####.'), # Right
        ])

        r2_edges = rotate(edges, 2)
        numpy.testing.assert_equal(r2_edges, expected_edges_2)

    def test_rotate_3(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)
        
        tile_id = 2311
        self.assertIn(tile_id, tile_map)

        edges = tile_map[tile_id]['edges']

        expected_edges_3 = np.array([
            list('.#..#####.'), # Top
            list('#..##.#...'), # Bottom
            list('..###..###'), # Left
            list('..##.#..#.'), # Right
        ])

        r3_edges = rotate(edges, 3)
        numpy.testing.assert_equal(r3_edges, expected_edges_3)

    def test_flip_n(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)
        
        tile_id = 2311
        self.assertIn(tile_id, tile_map)

        edges = tile_map[tile_id]['edges']

        expected_edges_n = np.array([
            list('..##.#..#.'), # Top
            list('..###..###'), # Bottom
            list('.#####..#.'), # Left
            list('...#.##..#'), # Right
        ])
        flipped_edges = flip_edges(edges, 'n')
        numpy.testing.assert_equal(
            flipped_edges, expected_edges_n
        )

    def test_flip_h(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)
        
        tile_id = 2311
        self.assertIn(tile_id, tile_map)

        edges = tile_map[tile_id]['edges']

        expected_edges_h = np.array([
            list('.#..#.##..'), # Top
            list('###..###..'), # Bottom
            list('...#.##..#'), # Left
            list('.#####..#.'), # Right
        ])
        flipped_edges = flip_edges(edges, 'h')
        numpy.testing.assert_equal(
            flipped_edges, expected_edges_h
        )

    def test_flip_v(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)
        
        tile_id = 2311
        self.assertIn(tile_id, tile_map)

        edges = tile_map[tile_id]['edges']

        expected_edges_v = np.array([
            list('..###..###'), # Top
            list('..##.#..#.'), # Bottom
            list('.#..#####.'), # Left
            list('#..##.#...'), # Right
        ])
        flipped_edges = flip_edges(edges, 'v')
        numpy.testing.assert_equal(
            flipped_edges, expected_edges_v
        )
    
    def test_compare_left(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)
        
        a_edges = flip_v(tile_map[2311]['edges'])
        b_edges = flip_v(tile_map[1951]['edges'])
        self.assertTrue(compare_tiles_relative(a_edges, b_edges, 'left'))

    def test_compare_right(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)
        
        a_edges = flip_v(tile_map[2311]['edges'])
        b_edges = tile_map[3079]['edges']
        self.assertTrue(compare_tiles_relative(a_edges, b_edges, 'right'))

    def test_compare_top(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)
        
        a_edges = flip_v(tile_map[2311]['edges'])
        b_edges = flip_v(tile_map[1427]['edges'])
        self.assertTrue(compare_tiles_relative(b_edges, a_edges, 'top'))

    def test_compare_bottom(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)
        
        a_edges = flip_v(tile_map[2311]['edges'])
        b_edges = flip_v(tile_map[1427]['edges'])
        self.assertTrue(compare_tiles_relative(a_edges, b_edges, 'bottom'))

    def test_reduce_neighbors_1951(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)

        tile_id = 1951
        actual_neighbors = {2729, 2311}
        potential_neighbors = tile_map[tile_id]['neighbors']
        for a in actual_neighbors:
            self.assertIn(a, potential_neighbors)

    def test_reduce_neighbors_2311(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)

        tile_id = 2311
        actual_neighbors = {1951, 1427, 3079}
        potential_neighbors = tile_map[tile_id]['neighbors']
        for a in actual_neighbors:
            self.assertIn(a, potential_neighbors)

    def test_reduce_neighbors_3079(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)

        tile_id = 3079
        actual_neighbors = {2473, 2311}
        potential_neighbors = tile_map[tile_id]['neighbors']
        for a in actual_neighbors:
            self.assertIn(a, potential_neighbors)

    def test_reduce_neighbors_2729(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)

        tile_id = 2729
        actual_neighbors = {1951, 1427, 2971}
        potential_neighbors = tile_map[tile_id]['neighbors']
        for a in actual_neighbors:
            self.assertIn(a, potential_neighbors)

    def test_reduce_neighbors_1427(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)

        tile_id = 1427
        actual_neighbors = {2311, 2729, 1489, 2473}
        potential_neighbors = tile_map[tile_id]['neighbors']
        for a in actual_neighbors:
            self.assertIn(a, potential_neighbors)

    def test_reduce_neighbors_2473(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)

        tile_id = 2473
        actual_neighbors = {3079, 1427, 1171}
        potential_neighbors = tile_map[tile_id]['neighbors']
        for a in actual_neighbors:
            self.assertIn(a, potential_neighbors)

    def test_reduce_neighbors_2971(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)

        tile_id = 2971
        actual_neighbors = {2729, 1489}
        potential_neighbors = tile_map[tile_id]['neighbors']
        for a in actual_neighbors:
            self.assertIn(a, potential_neighbors)

    def test_reduce_neighbors_1489(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)

        tile_id = 1489
        actual_neighbors = {2971, 1427, 1171}
        potential_neighbors = tile_map[tile_id]['neighbors']
        for a in actual_neighbors:
            self.assertIn(a, potential_neighbors)

    def test_reduce_neighbors_1171(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)

        tile_id = 1171
        actual_neighbors = {1489, 2473}
        potential_neighbors = tile_map[tile_id]['neighbors']
        for a in actual_neighbors:
            self.assertIn(a, potential_neighbors)

    def test_match_2473(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)

        tile_id = 2473
        expected_tile = np.array([
            list('#....####.'),
            list('#..#.##...'),
            list('#.##..#...'),
            list('######.#.#'),
            list('.#...#.#.#'),
            list('.#########'),
            list('.###.#..#.'),
            list('########.#'),
            list('##...##.#.'),
            list('..###.#.#.'),
        ])
        grid = tiles[tile_id]
        numpy.testing.assert_equal(expected_tile, grid)

        rotated_grid = np.array([
            list('..#.###...'),
            list('##.##....#'),
            list('..#.###..#'),
            list('###.#..###'),
            list('.######.##'),
            list('#.#.#.#...'),
            list('#.###.###.'),
            list('#.###.##..'),
            list('.######...'),
            list('.##...####'),
        ])

        rotated_edges = np.array([
            list('..#.###...'),
            list('.##...####'),
            list('.#.#.###..'),
            list('.####....#'),
        ])

        edges = tile_map[tile_id]['edges']
        #edges = flip_v(flip_h(tile_map[tile_id]['edges']))
        edges = handle_rotation_flip(edges, 1, 'h')
        #edges = rotate(edges, 1)
        #edges = flip_h(edges)
        np.testing.assert_equal(rotated_edges, edges)


    def test_match_2473_to_1171(self):
        filename = 'example1.txt'
        tiles = load_data(filename)
        tile_map = reduce_tiles(tiles)

        a_tile_id = 2473
        b_tile_id = 1171
        #a_tile = handle_rotation_flip(a_tile_id)
