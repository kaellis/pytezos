from tests.templates import opcode_test_case
from os.path import dirname, join, exists
from os import mkdir

# Merci beaucoup a @arvidnl et tout le monde

parameterized_data = [
    # FORMAT: assert_output contract_file storage input expected_result

    # TODO add tests for map_car.tz, subset.tz
    # NB: noop.tz is tested in test_basic.sh

    ('cons.tz', '{}', '10', '{ 10 }'),
    ('cons.tz', '{ 10 }', '-5', '{ -5 ; 10 }'),
    ('cons.tz', '{ -5 ; 10 }', '99', '{ 99 ; -5 ; 10 }'),

    # Tests on Options
    ('none.tz', 'Some 10', 'Unit', 'None'),

    ('ret_int.tz', 'None', 'Unit', '(Some 300)'),

    # Map block on lists
    ('list_map_block.tz', '{0}', '{}', '{}'),
    ('list_map_block.tz', '{0}', '{ 1 ; 1 ; 1 ; 1 }',
     '{ 1 ; 2 ; 3 ; 4 }'),
    ('list_map_block.tz', '{0}', '{ 1 ; 2 ; 3 ; 0 }',
     '{ 1 ; 3 ; 5 ; 3 }'),

    # Reverse a list
    ('reverse.tz', '{""}', '{}', '{}'),
    ('reverse.tz', '{""}', '{ "c" ; "b" ; "a" }',
     '{ "a" ; "b" ; "c" }'),

    # Reverse using LOOP_LEFT
    ('loop_left.tz', '{""}', '{}', '{}'),
    ('loop_left.tz', '{""}', '{ "c" ; "b" ; "a" }',
     '{ "a" ; "b" ; "c" }'),

    # Identity on strings
    ('str_id.tz', 'None', '"Hello"', '(Some "Hello")'),
    ('str_id.tz', 'None', '"abcd"', '(Some "abcd")'),

    # Slice strings
    ('slice.tz', 'None', 'Pair 0 0', 'None'),
    ('slice.tz', 'Some "Foo"', 'Pair 10 5', 'None'),
    ('slice.tz', 'Some "Foo"', 'Pair 0 0', '(Some "")'),
    ('slice.tz', 'Some "Foo"', 'Pair 0 10', 'None'),
    ('slice.tz', 'Some "Foo"', 'Pair 0 2', '(Some "Fo")'),
    ('slice.tz', 'Some "Foo"', 'Pair 1 3', 'None'),
    ('slice.tz', 'Some "Foo"', 'Pair 1 1', '(Some "o")'),

    # Slice bytes
    ('slice_bytes.tz', 'None', '(Pair 0 1)', 'None'),
    ('slice_bytes.tz', '(Some 0xaabbcc)', '(Pair 0 0)', '(Some 0x)'),
    ('slice_bytes.tz', '(Some 0xaabbcc)', '(Pair 0 1)', '(Some 0xaa)'),
    ('slice_bytes.tz', '(Some 0xaabbcc)', '(Pair 1 1)', '(Some 0xbb)'),
    ('slice_bytes.tz', '(Some 0xaabbcc)', '(Pair 1 2)', '(Some 0xbbcc)'),
    ('slice_bytes.tz', '(Some 0xaabbcc)', '(Pair 1 3)', 'None'),
    ('slice_bytes.tz', '(Some 0xaabbcc)', '(Pair 1 1)', '(Some 0xbb)'),

    # Identity on pairs
    ('pair_id.tz', 'None', '(Pair True False)',
     '(Some (Pair True False))'),
    ('pair_id.tz', 'None', '(Pair False True)',
     '(Some (Pair False True))'),
    ('pair_id.tz', 'None', '(Pair True True)',
     '(Some (Pair True True))'),
    ('pair_id.tz', 'None', '(Pair False False)',
     '(Some (Pair False False))'),

    # Tests CAR and CDR instructions
    ('car.tz', '0', '(Pair 34 17)', '34'),
    ('cdr.tz', '0', '(Pair 34 17)', '17'),

    # Logical not
    ('not.tz', 'None', 'True', '(Some False)'),
    ('not.tz', 'None', 'False', '(Some True)'),

    # Logical and
    ('and.tz', 'None', '(Pair False False)', '(Some False)'),
    ('and.tz', 'None', '(Pair False True)', '(Some False)'),
    ('and.tz', 'None', '(Pair True False)', '(Some False)'),
    ('and.tz', 'None', '(Pair True True)', '(Some True)'),

    # Logical or
    ('or.tz', 'None', '(Pair False False)', '(Some False)'),
    ('or.tz', 'None', '(Pair False True)', '(Some True)'),
    ('or.tz', 'None', '(Pair True False)', '(Some True)'),
    ('or.tz', 'None', '(Pair True True)', '(Some True)'),

    # Logical and
    ('and_logical_1.tz', 'False', "(Pair False False)", 'False'),
    ('and_logical_1.tz', 'False', "(Pair False True)", 'False'),
    ('and_logical_1.tz', 'False', "(Pair True False)", 'False'),
    ('and_logical_1.tz', 'False', "(Pair True True)", 'True'),

    # Binary and
    ('and_binary.tz', 'Unit', 'Unit', 'Unit'),


    # Binary or
    ('or_binary.tz', 'None', '(Pair 4 8)', '(Some 12)'),
    ('or_binary.tz', 'None', '(Pair 0 8)', '(Some 8)'),
    ('or_binary.tz', 'None', '(Pair 8 0)', '(Some 8)'),
    ('or_binary.tz', 'None', '(Pair 15 4)', '(Some 15)'),
    ('or_binary.tz', 'None', '(Pair 14 1)', '(Some 15)'),
    ('or_binary.tz', 'None', '(Pair 7 7)', '(Some 7)'),

    # Binary not
    ('not_binary.tz', 'None', '(Left 0)', '(Some -1)'),
    ('not_binary.tz', 'None', '(Left 8)', '(Some -9)'),
    ('not_binary.tz', 'None', '(Left 7)', '(Some -8)'),
    ('not_binary.tz', 'None', '(Left -9)', '(Some 8)'),
    ('not_binary.tz', 'None', '(Left -8)', '(Some 7)'),

    ('not_binary.tz', 'None', '(Right 0)', '(Some -1)'),
    ('not_binary.tz', 'None', '(Right 8)', '(Some -9)'),
    ('not_binary.tz', 'None', '(Right 7)', '(Some -8)'),

    # XOR
    ('xor.tz', 'None', '(Left (Pair False False))',
     '(Some (Left False))'),
    ('xor.tz', 'None', '(Left (Pair False True))',
     '(Some (Left True))'),
    ('xor.tz', 'None', '(Left (Pair True False))',
     '(Some (Left True))'),
    ('xor.tz', 'None', '(Left (Pair True True))',
     '(Some (Left False))'),

    ('xor.tz', 'None', '(Right (Pair 0 0))', '(Some (Right 0))'),
    ('xor.tz', 'None', '(Right (Pair 0 1))', '(Some (Right 1))'),
    ('xor.tz', 'None', '(Right (Pair 1 0))', '(Some (Right 1))'),
    ('xor.tz', 'None', '(Right (Pair 1 1))', '(Some (Right 0))'),
    ('xor.tz', 'None', '(Right (Pair 42 21))', '(Some (Right 63))'),
    ('xor.tz', 'None', '(Right (Pair 42 63))', '(Some (Right 21))'),

    # test shifts: LSL & LSR
    ('shifts.tz', 'None', '(Left (Pair 8 1))', '(Some 16)'),
    ('shifts.tz', 'None', '(Left (Pair 0 0))', '(Some 0)'),
    ('shifts.tz', 'None', '(Left (Pair 0 1))', '(Some 0)'),
    ('shifts.tz', 'None', '(Left (Pair 1 2))', '(Some 4)'),
    ('shifts.tz', 'None', '(Left (Pair 15 2))', '(Some 60)'),

    ('shifts.tz', 'None', '(Right (Pair 8 1))', '(Some 4)'),
    ('shifts.tz', 'None', '(Right (Pair 0 0))', '(Some 0)'),
    ('shifts.tz', 'None', '(Right (Pair 0 1))', '(Some 0)'),
    ('shifts.tz', 'None', '(Right (Pair 1 2))', '(Some 0)'),
    ('shifts.tz', 'None', '(Right (Pair 15 2))', '(Some 3)'),

    # Concatenate all strings of a list into one string
    ('concat_list.tz', '""', '{ "a" ; "b" ; "c" }', '"abc"'),
    ('concat_list.tz', '""', '{}', '""'),
    ('concat_list.tz', '""', '{ "Hello" ; " " ; "World" ; "!" }',
     '"Hello World!"'),

    # Concatenate the bytes in storage with all bytes in the given list
    ('concat_hello_bytes.tz', '{}', '{ 0xcd }',
     '{ 0xffcd }'),
    ('concat_hello_bytes.tz', '{}', '{}',
     '{}'),
    ('concat_hello_bytes.tz', '{}', '{ 0xab ; 0xcd }',
     '{ 0xffab ; 0xffcd }'),

    # Identity on lists
    ('list_id.tz', '{""}', '{ "1" ; "2" ; "3" }',
     '{ "1" ; "2" ; "3" }'),
    ('list_id.tz', '{""}', '{}', '{}'),
    ('list_id.tz', '{""}', '{ "a" ; "b" ; "c" }',
     '{ "a" ; "b" ; "c" }'),

    ('list_id_map.tz', '{""}', '{ "1" ; "2" ; "3" }',
     '{ "1" ; "2" ; "3" }'),
    ('list_id_map.tz', '{""}', '{}', '{}'),
    ('list_id_map.tz', '{""}', '{ "a" ; "b" ; "c" }',
     '{ "a" ; "b" ; "c" }'),


    # Identity on maps
    ('map_id.tz', '{}', '{ Elt 0 1 }', '{ Elt 0 1 }'),
    ('map_id.tz', '{}', '{ Elt 0 0 }', '{ Elt 0 0 }'),
    ('map_id.tz', '{}', '{ Elt 0 0 ; Elt 3 4 }',
     '{ Elt 0 0 ; Elt 3 4 }'),

    # Memberships in maps
    ('map_mem_nat.tz', '(Pair { Elt 0 1 } None)', '1',
     '(Pair { Elt 0 1 } (Some False))'),
    ('map_mem_nat.tz', '(Pair {} None)', '1',
     '(Pair {} (Some False))'),
    ('map_mem_nat.tz', '(Pair { Elt 1 0 } None)', '1',
     '(Pair { Elt 1 0 } (Some True))'),
    ('map_mem_nat.tz', '(Pair { Elt 1 4 ; Elt 2 11 } None)', '1',
     '(Pair { Elt 1 4 ; Elt 2 11 } (Some True))'),
    ('map_mem_nat.tz', '(Pair { Elt 1 4 ; Elt 2 11 } None)', '2',
     '(Pair { Elt 1 4 ; Elt 2 11 } (Some True))'),
    ('map_mem_nat.tz', '(Pair { Elt 1 4 ; Elt 2 11 } None)', '3',
     '(Pair { Elt 1 4 ; Elt 2 11 } (Some False))'),

    ('map_mem_string.tz', '(Pair { Elt "foo" 1 } None)', '"bar"',
     '(Pair { Elt "foo" 1 } (Some False))'),
    ('map_mem_string.tz', '(Pair {} None)', '"bar"',
     '(Pair {} (Some False))'),
    ('map_mem_string.tz', '(Pair { Elt "foo" 0 } None)', '"foo"',
     '(Pair { Elt "foo" 0 } (Some True))'),
    ('map_mem_string.tz', '(Pair { Elt "bar" 4 ; Elt "foo" 11 } None)',
     '"foo"', '(Pair { Elt "bar" 4 ; Elt "foo" 11 } (Some True))'),
    ('map_mem_string.tz', '(Pair { Elt "bar" 4 ; Elt "foo" 11 } None)',
     '"bar"', '(Pair { Elt "bar" 4 ; Elt "foo" 11 } (Some True))'),
    ('map_mem_string.tz', '(Pair { Elt "bar" 4 ; Elt "foo" 11 } None)',
     '"baz"', '(Pair { Elt "bar" 4 ; Elt "foo" 11 } (Some False))'),

    # Mapping over maps
    ('map_map.tz', '{}', '10', '{}'),
    ('map_map.tz', '{ Elt "foo" 1 }', '10', '{ Elt "foo" 11 }'),
    ('map_map.tz', '{ Elt "bar" 5 ; Elt "foo" 1 }', '15',
     '{ Elt "bar" 20 ; Elt "foo" 16 }'),

    # Memberships in big maps
    ('big_map_mem_nat.tz', '(Pair { Elt 0 1 } None)', '1',
     '(Pair 0 (Some False))'),
    ('big_map_mem_nat.tz', '(Pair {} None)', '1',
     '(Pair 0 (Some False))'),
    ('big_map_mem_nat.tz', '(Pair { Elt 1 0 } None)', '1',
     '(Pair 0 (Some True))'),
    ('big_map_mem_nat.tz', '(Pair { Elt 1 4 ; Elt 2 11 } None)', '1',
     '(Pair 0 (Some True))'),
    ('big_map_mem_nat.tz', '(Pair { Elt 1 4 ; Elt 2 11 } None)', '2',
     '(Pair 0 (Some True))'),
    ('big_map_mem_nat.tz', '(Pair { Elt 1 4 ; Elt 2 11 } None)', '3',
     '(Pair 0 (Some False))'),

    ('big_map_mem_string.tz',
     '(Pair { Elt "foo" 1 } None)', '"bar"',
     '(Pair 0 (Some False))'),
    ('big_map_mem_string.tz',
     '(Pair {} None)', '"bar"',
     '(Pair 0 (Some False))'),
    ('big_map_mem_string.tz',
     '(Pair { Elt "foo" 0 } None)', '"foo"',
     '(Pair 0 (Some True))'),
    ('big_map_mem_string.tz',
     '(Pair { Elt "bar" 4 ; Elt "foo" 11 } None)',
     '"foo"', '(Pair 0 (Some True))'),
    ('big_map_mem_string.tz',
     '(Pair { Elt "bar" 4 ; Elt "foo" 11 } None)',
     '"bar"', '(Pair 0 (Some True))'),
    ('big_map_mem_string.tz',
     '(Pair { Elt "bar" 4 ; Elt "foo" 11 } None)',
     '"baz"', '(Pair 0 (Some False))'),

    # Memberships in big maps
    ('big_map_mem_nat.tz', '(Pair { Elt 0 1 } None)', '1',
     '(Pair 0 (Some False))'),
    ('big_map_mem_nat.tz', '(Pair {} None)', '1',
     '(Pair 0 (Some False))'),
    ('big_map_mem_nat.tz', '(Pair { Elt 1 0 } None)', '1',
     '(Pair 0 (Some True))'),
    ('big_map_mem_nat.tz', '(Pair { Elt 1 4 ; Elt 2 11 } None)', '1',
     '(Pair 0 (Some True))'),
    ('big_map_mem_nat.tz', '(Pair { Elt 1 4 ; Elt 2 11 } None)', '2',
     '(Pair 0 (Some True))'),
    ('big_map_mem_nat.tz', '(Pair { Elt 1 4 ; Elt 2 11 } None)', '3',
     '(Pair 0 (Some False))'),

    # Identity on sets
    ('set_id.tz', '{}', '{ "a" ; "b" ; "c" }', '{ "a" ; "b" ; "c" }'),
    ('set_id.tz', '{}', '{}', '{}'),
    ('set_id.tz', '{}', '{ "asdf" ; "bcde" }', '{ "asdf" ; "bcde" }'),

    # List concat
    ('list_concat.tz', '"abc"', '{ "d" ; "e" ; "f" }', '"abcdef"'),
    ('list_concat.tz', '"abc"', '{}', '"abc"'),

    ('list_concat_bytes.tz', '0x00ab', '{ 0xcd ; 0xef ; 0x00 }',
     '0x00abcdef00'),
    ('list_concat_bytes.tz', '0x', '{ 0x00 ; 0x11 ; 0x00 }',
     '0x001100'),
    ('list_concat_bytes.tz', '0xabcd', '{}', '0xabcd'),
    ('list_concat_bytes.tz', '0x', '{}', '0x'),

    # List iter
    ('list_iter.tz', '0', '{ 10 ; 2 ; 1 }', '20'),
    ('list_iter.tz', '0', '{ 3 ; 6 ; 9 }', '162'),

    # List size
    ('list_size.tz', '111', '{}', '0'),
    ('list_size.tz', '111', '{ 1 }', '1'),
    ('list_size.tz', '111', '{ 1 ; 2 ; 3 }', '3'),
    ('list_size.tz', '111', '{ 1 ; 2 ; 3 ; 4 ; 5 ; 6 }', '6'),

    # Set member -- set is in storage
    ('set_member.tz', '(Pair {} None)', '"Hi"',
     '(Pair {} (Some False))'),
    ('set_member.tz', '(Pair { "Hi" } None)', '"Hi"',
     '(Pair { "Hi" } (Some True))'),
    ('set_member.tz', '(Pair { "Hello" ; "World" } None)', '""',
     '(Pair { "Hello" ; "World" } (Some False))'),

    # Set size
    ('set_size.tz', '111', '{}', '0'),
    ('set_size.tz', '111', '{ 1 }', '1'),
    ('set_size.tz', '111', '{ 1 ; 2 ; 3 }', '3'),
    ('set_size.tz', '111', '{ 1 ; 2 ; 3 ; 4 ; 5 ; 6 }', '6'),

    # Set iter
    ('set_iter.tz', '111', '{}', '0'),
    ('set_iter.tz', '111', '{ 1 }', '1'),
    ('set_iter.tz', '111', '{ -100 ; 1 ; 2 ; 3 }', '-94'),

    # Map size
    ('map_size.tz', '111', '{}', '0'),
    ('map_size.tz', '111', '{ Elt "a" 1 }', '1'),
    ('map_size.tz', '111', '{ Elt "a" 1 ; Elt "b" 2 ; Elt "c" 3 }',
     '3'),
    ('map_size.tz', '111', '{ Elt "a" 1 ; Elt "b" 2 ; Elt "c" 3 ; \
    Elt "d" 4 ; Elt "e" 5 ; Elt "f" 6 }',
     '6'),

    # Contains all elements -- does the second list contain
    # all of the same elements as the first one? I'm ignoring
    # element multiplicity
    ('contains_all.tz', 'None', '(Pair {} {})',
     '(Some True)'),
    ('contains_all.tz', 'None', '(Pair { "a" } { "B" })',
     '(Some False)'),
    ('contains_all.tz', 'None', '(Pair { "A" } { "B" })',
     '(Some False)'),
    ('contains_all.tz', 'None', '(Pair { "B" } { "B" })',
     '(Some True)'),
    ('contains_all.tz', 'None',
     '(Pair { "B" ; "C" ; "asdf" } { "B" ; "B" ; "asdf" ; "C" })',
     '(Some True)'),
    ('contains_all.tz', 'None',
     '(Pair { "B" ; "B" ; "asdf" ; "C" } { "B" ; "C" ; "asdf" })',
     '(Some True)'),

    # Concatenate the string in storage with all strings in
    # the given list
    ('concat_hello.tz', '{}', '{ "World!" }', '{ "Hello World!" }'),
    ('concat_hello.tz', '{}', '{}', '{}'),
    ('concat_hello.tz', '{}', '{ "test1" ; "test2" }',
     '{ "Hello test1" ; "Hello test2" }'),

    # Create an empty map and add a string to it
    ('empty_map.tz', '{}', 'Unit', '{ Elt "hello" "world" }'),

    # Get the value stored at the given key in the map
    ('get_map_value.tz', '(Pair None { Elt "hello" "hi" })',
     '"hello"', '(Pair (Some "hi") { Elt "hello" "hi" })'),
    ('get_map_value.tz', '(Pair None { Elt "hello" "hi" })',
     '""', '(Pair None { Elt "hello" "hi" })'),
    ('get_map_value.tz', '(Pair None { Elt "1" "one" ; \
    Elt "2" "two" })',
     '"1"', '(Pair (Some "one") { Elt "1" "one" ; Elt "2" "two" })'),

    # Map iter
    ('map_iter.tz', '(Pair 0 0)', '{ Elt 0 100 ; Elt 2 100 }',
     '(Pair 2 200)'),
    ('map_iter.tz', '(Pair 0 0)', '{ Elt 1 1 ; Elt 2 100 }',
     '(Pair 3 101)'),

    # Return True if True branch of if was taken and False otherwise
    ('if.tz', 'None', 'True', '(Some True)'),
    ('if.tz', 'None', 'False', '(Some False)'),

    # Generate a pair of or types
    ('left_right.tz', '(Left "X")', '(Left True)', '(Right True)'),
    ('left_right.tz', '(Left "X")', '(Right "a")', '(Left "a")'),

    # Reverse a list
    ('reverse_loop.tz', '{""}', '{}', '{}'),
    ('reverse_loop.tz', '{""}', '{ "c" ; "b" ; "a" }',
     '{ "a" ; "b" ; "c" }'),

    # Exec concat contract
    ('exec_concat.tz', '"?"', '""', '"_abc"'),
    ('exec_concat.tz', '"?"', '"test"', '"test_abc"'),

    # Get the current balance of the contract
    ('balance.tz', '111', 'Unit', '4000000000000'),

    # Test addition and subtraction on tez
    ('tez_add_sub.tz', 'None', '(Pair 2000000 1000000)',
     '(Some (Pair 3000000 1000000))'),
    ('tez_add_sub.tz', 'None', '(Pair 2310000 1010000)',
     '(Some (Pair 3320000 1300000))'),

    # Test various additions
    ('add.tz', 'Unit', 'Unit', 'Unit'),

    # Test ABS
    ('abs.tz', 'Unit', '12039123919239192312931', 'Unit'),
    ('abs.tz', 'Unit', '0', 'Unit'),
    ('abs.tz', 'Unit', '948', 'Unit'),

    # Test INT
    ('int.tz', 'None', '0', '(Some 0)'),
    ('int.tz', 'None', '1', '(Some 1)'),
    ('int.tz', 'None', '9999', '(Some 9999)'),

    # Test DIP
    ('dip.tz', '(Pair 0 0)', '(Pair 15 9)', '(Pair 15 24)'),
    ('dip.tz', '(Pair 0 0)', '(Pair 1 1)', '(Pair 1 2)'),

    # Test get first element of list
    ('first.tz', '111', '{ 1 ; 2 ; 3 ; 4 }', '1'),
    ('first.tz', '111', '{ 4 }', '4'),

    # Hash input string
    # Test assumed to be correct -- hash is based on encoding of AST
    ('hash_string.tz', '0x00', '"abcdefg"', '0x46fdbcb4ea4eadad5615c' +
     'daa17d67f783e01e21149ce2b27de497600b4cd8f4e'),
    ('hash_string.tz', '0x00', '"12345"', '0xb4c26c20de52a4eaf0d8a34' +
     '0db47ad8cb1e74049570859c9a9a3952b204c772f'),

    # IF_SOME
    ('if_some.tz', '"?"', '(Some "hello")', '"hello"'),
    ('if_some.tz', '"?"', 'None', '""'),

    # Tests the SET_CAR and SET_CDR instructions
    ('set_car.tz', '(Pair "hello" 0)', '"world"', '(Pair "world" 0)'),
    ('set_car.tz', '(Pair "hello" 0)', '"abc"', '(Pair "abc" 0)'),
    ('set_car.tz', '(Pair "hello" 0)', '""', '(Pair "" 0)'),

    ('set_cdr.tz', '(Pair "hello" 0)', '1', '(Pair "hello" 1)'),
    ('set_cdr.tz', '(Pair "hello" 500)', '3', '(Pair "hello" 3)'),
    ('set_cdr.tz', '(Pair "hello" 7)', '100', '(Pair "hello" 100)'),

    # Convert a public key to a public key hash
    ('hash_key.tz', 'None',
     '"edpkuBknW28nW72KG6RoHtYW7p12T6GKc7nAbwYX5m8Wd9sDVC9yav"',
     '(Some "tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx")'),
    ('hash_key.tz', 'None',
     '"edpkuJqtDcA2m2muMxViSM47MPsGQzmyjnNTawUPqR8vZTAMcx61ES"',
     '(Some "tz1XPTDmvT3vVE5Uunngmixm7gj7zmdbPq6k")'),

    # Test timestamp operations
    ('add_timestamp_delta.tz', 'None',
     '(Pair 100 100)', '(Some "1970-01-01T00:03:20Z")'),
    ('add_timestamp_delta.tz', 'None',
     '(Pair 100 -100)', '(Some "1970-01-01T00:00:00Z")'),
    ('add_timestamp_delta.tz', 'None',
     '(Pair "1970-01-01T00:00:00Z" 0)',
     '(Some "1970-01-01T00:00:00Z")'),

    ('add_delta_timestamp.tz', 'None',
     '(Pair 100 100)', '(Some "1970-01-01T00:03:20Z")'),
    ('add_delta_timestamp.tz', 'None',
     '(Pair -100 100)', '(Some "1970-01-01T00:00:00Z")'),
    ('add_delta_timestamp.tz', 'None',
     '(Pair 0 "1970-01-01T00:00:00Z")',
     '(Some "1970-01-01T00:00:00Z")'),

    ('sub_timestamp_delta.tz', '111', '(Pair 100 100)',
     '"1970-01-01T00:00:00Z"'),
    ('sub_timestamp_delta.tz', '111', '(Pair 100 -100)',
     '"1970-01-01T00:03:20Z"'),
    ('sub_timestamp_delta.tz', '111', '(Pair 100 2000000000000000000)',
     '-1999999999999999900'),

    ('diff_timestamps.tz', '111', '(Pair 0 0)', '0'),
    ('diff_timestamps.tz', '111', '(Pair 0 1)', '-1'),
    ('diff_timestamps.tz', '111', '(Pair 1 0)', '1'),
    ('diff_timestamps.tz', '111',
     '(Pair "1970-01-01T00:03:20Z" "1970-01-01T00:00:00Z")', '200'),

    # Test pack/unpack
    ('packunpack_rev.tz', 'Unit',
     '(Pair -1  (Pair 1 (Pair "foobar" (Pair 0x00AABBCC (Pair 1000 ' +
     '(Pair False (Pair "tz1cxcwwnzENRdhe2Kb8ZdTrdNy4bFNyScx5" ' +
     '(Pair "2019-09-09T08:35:33Z" ' +
     '"tz1cxcwwnzENRdhe2Kb8ZdTrdNy4bFNyScx5"))))))))', 'Unit'),

    ('packunpack_rev.tz', 'Unit',
     '(Pair -1  (Pair 1 (Pair "foobar" (Pair 0x00AABBCC (Pair 1000 ' +
     '(Pair False (Pair "tz1cxcwwnzENRdhe2Kb8ZdTrdNy4bFNyScx5" ' +
     '(Pair "2019-09-09T08:35:33Z" ' +
     '"tz1cxcwwnzENRdhe2Kb8ZdTrdNy4bFNyScx5"))))))))', 'Unit'),

    ('packunpack_rev_cty.tz', 'Unit',
     '(Pair "edpkuBknW28nW72KG6RoHtYW7p12T6GKc7nAbwYX5m8Wd9' +
     'sDVC9yav" (Pair Unit (Pair "edsigthTzJ8X7MPmNeEwybRAv' +
     'dxS1pupqcM5Mk4uCuyZAe7uEk68YpuGDeViW8wSXMrCi5CwoNgqs8' +
     'V2w8ayB5dMJzrYCHhD8C7" (Pair (Some "edsigthTzJ8X7MPmN' +
     'eEwybRAvdxS1pupqcM5Mk4uCuyZAe7uEk68YpuGDeViW8wSXMrCi5' +
     'CwoNgqs8V2w8ayB5dMJzrYCHhD8C7") (Pair { Unit }  (Pair' +
     ' { True }  (Pair (Pair 19 10) (Pair (Left "tz1cxcwwnz' +
     'ENRdhe2Kb8ZdTrdNy4bFNyScx5") (Pair { Elt 0 "foo" ; El' +
     't 1 "bar" }  { PACK } )))))))))',
     'Unit'),

    ('packunpack_rev_cty.tz', 'Unit',
     '(Pair "edpkuBknW28nW72KG6RoHtYW7p12T6GKc7nAbwYX5m8Wd9' +
     'sDVC9yav" (Pair Unit (Pair "edsigthTzJ8X7MPmNeEwybRAv' +
     'dxS1pupqcM5Mk4uCuyZAe7uEk68YpuGDeViW8wSXMrCi5CwoNgqs8' +
     'V2w8ayB5dMJzrYCHhD8C7" (Pair None (Pair {  }  (Pair {' +
     '  }  (Pair (Pair 40 -10) (Pair (Right "2019-09-09T08:' +
     '35:33Z") (Pair {  }  { DUP ; DROP ; PACK } )))))))))',
     'Unit'),

    # Test EDIV on nat and int
    ('ediv.tz',
     '(Pair None (Pair None (Pair None None)))',
     '(Pair 10 -3)',
     '(Pair (Some (Pair -3 1)) (Pair (Some (Pair 3 1)) ' +
     '(Pair (Some (Pair -3 1)) (Some (Pair 3 1)))))'),
    ('ediv.tz',
     '(Pair None (Pair None (Pair None None)))',
     '(Pair 10 0)',
     '(Pair None (Pair None (Pair None None)))'),
    ('ediv.tz',
     '(Pair None (Pair None (Pair None None)))',
     '(Pair -8 2)',
     '(Pair (Some (Pair -4 0)) (Pair (Some (Pair -4 0)) ' +
     '(Pair (Some (Pair 4 0)) (Some (Pair 4 0)))))'),

    # Test EDIV on mutez
    ('ediv_mutez.tz', '(Left None)', '(Pair 10 (Left 10))',
     '(Left (Some (Pair 1 0)))'),
    ('ediv_mutez.tz', '(Left None)', '(Pair 10 (Left 3))',
     '(Left (Some (Pair 3 1)))'),
    ('ediv_mutez.tz', '(Left None)', '(Pair 10 (Left 0))',
     '(Left None)'),

    ('ediv_mutez.tz', '(Left None)', '(Pair 10 (Right 10))',
     '(Right (Some (Pair 1 0)))'),
    ('ediv_mutez.tz', '(Left None)', '(Pair 10 (Right 3))',
     '(Right (Some (Pair 3 1)))'),
    ('ediv_mutez.tz', '(Left None)', '(Pair 10 (Right 0))',
     '(Right None)'),
    ('ediv_mutez.tz', '(Left None)', '(Pair 5 (Right 10))',
     '(Right (Some (Pair 0 5)))'),

    # Test compare
    ('compare.tz', 'Unit', 'Unit', 'Unit'),

    # Test comparison combinators:
    #   GT, GE, LT, LE, NEQ, EQ

    ('comparisons.tz', '{}',
     '{ -9999999; -1 ; 0 ; 1 ; 9999999 }',
     '{ ' +
     '{ False ; False ; False ; True ; True } ;' "\n"
     '    { False ; False ; True ; True ; True } ;' "\n"
     '    { True ; True ; False ; False ; False } ;' "\n"
     '    { True ; True ; True ; False ; False } ;' "\n"
     '    { True ; True ; False ; True ; True } ;' "\n"
     '    { False ; False ; True ; False ; False }'
     ' }'),

    # Test ADDRESS
    ('address.tz', 'None', '"tz1cxcwwnzENRdhe2Kb8ZdTrdNy4bFNyScx5"',
     '(Some "tz1cxcwwnzENRdhe2Kb8ZdTrdNy4bFNyScx5")'),

    # Test (CONTRACT unit)
    ('contract.tz', 'Unit', '"tz1cxcwwnzENRdhe2Kb8ZdTrdNy4bFNyScx5"',
     'Unit'),

    # Test create_contract
    ('create_contract.tz', 'None', 'Unit',
     '(Some "KT1Mjjcb6tmSsLm7Cb3DSQszePjfchPM4Uxm")'),

    # Test multiplication - success case (no overflow)
    # Failure case is tested in m̀ul_overflow.tz
    ('mul.tz', 'Unit', 'Unit', 'Unit'),

    # Test NEG
    ('neg.tz', '0', '(Left 2)', '-2'),
    ('neg.tz', '0', '(Right 2)', '-2'),
    ('neg.tz', '0', '(Left 0)', '0'),
    ('neg.tz', '0', '(Right 0)', '0'),
    ('neg.tz', '0', '(Left -2)', '2'),

    # Test DIGN, DUGN, DROPN, DIPN
    ('dign.tz', '0', '(Pair (Pair (Pair (Pair 1 2) 3) 4) 5)', '5'),
    ('dugn.tz', '0', '(Pair (Pair (Pair (Pair 1 2) 3) 4) 5)', '1'),
    ('dropn.tz', '0', '(Pair (Pair (Pair (Pair 1 2) 3) 4) 5)', '5'),
    ('dipn.tz', '0', '(Pair (Pair (Pair (Pair 1 2) 3) 4) 5)', '6'),

    # Test DIGN 17 times.
    ('dig_eq.tz',
     'Unit',
     '(Pair 17 (Pair 16 (Pair 15 (Pair 14 (Pair 13 (Pair 12' +
     ' (Pair 11 (Pair 10 (Pair 9 (Pair 8 (Pair 7 (Pair 6 (P' +
     'air 5 (Pair 4 (Pair 3 (Pair 2 1))))))))))))))))',
     'Unit'),
    ('dig_eq.tz',
     'Unit',
     '(Pair 2 (Pair 3 (Pair 12 (Pair 16 (Pair 10 (Pair 14 (' +
     'Pair 19 (Pair 9 (Pair 18 (Pair 6 (Pair 8 (Pair 11 (Pa' +
     'ir 4 (Pair 13 (Pair 15 (Pair 5 1))))))))))))))))',
     'Unit'),

    # Test Partial Exec
    ('pexec.tz', '14', '38', '52'),
    ('pexec_2.tz', "{ 0 ; 1 ; 2 ; 3}", '4', "{ 0 ; 7 ; 14 ; 21 }"),

    # Test CHAIN_ID
    ('chain_id_store.tz', 'None', 'Unit', '(Some 0x7a06a770)'),

    # Test SELF
    ('self_with_entrypoint.tz', 'Unit', 'Left (Left 0)', 'Unit'),
    ('self_with_default_entrypoint.tz', 'Unit', 'Unit', 'Unit')
]


def wrap(data):
    data = data.replace('\n', ' ')
    if any(map(data.startswith, ['Left', 'Right', 'Some', 'Pair'])):
        return f'({data})'
    else:
        return data


def make_opcode_tests():
    proj_dir = dirname(dirname(__file__))
    cases_dir = join(proj_dir, 'tests', 'opcodes', 'cases')
    if not exists(cases_dir):
        mkdir(cases_dir)

    contracts_dir = join(proj_dir, 'tests', 'opcodes', 'contracts')
    for i, (filename, storage, parameter, expected) in enumerate(parameterized_data):
        case = filename.replace(".tz", f'_{i}')
        body = opcode_test_case.format(
            case=case,
            filename=join(contracts_dir, filename),
            parameter=wrap(parameter),
            storage=wrap(storage),
            expected=wrap(expected)
        )
        with open(join(cases_dir, f'test_{case}.py'), 'w+') as f:
            f.write(body)


if __name__ == '__main__':
    make_opcode_tests()
