import chess
import chess.uci
import chess.pgn
import sys
import time

arguments = sys.argv
pgnfilename = str(arguments[1])

#Read pgn file:
with open(pgnfilename) as f:

    while True:
        try:
            game = chess.pgn.read_game(f)

            #Go to the end of the game and create a chess.Board() from it:
            game = game.end()
            board = game.board()

            #So if you want, here's also your PGN to FEN conversion:
            print 'FEN of the last position of the game: ', board.fen()

            #Now we have our board ready, load your engine:
            handler = chess.uci.InfoHandler()
            engine = chess.uci.popen_engine('Sf2') #give correct address of your engine here
            engine.info_handlers.append(handler)

            #give your position to the engine:
            engine.position(board)


            #time.sleep(0.1) # Time in seconds.

            # Set number of threads
            engine.setoption({"Threads": 68})
            #engine.setoption({"Threads": 1})
            engine.setoption({"MultiPV": 3})

            #Set your evaluation time, in ms:
            evaltime = 5000 #so 5 seconds
            #evaluation = engine.go(movetime=evaltime)
            evaluation = engine.go(depth=27)

            node = game

            #print board
            #print board.fen()
            #print board.result()
#
            #game.headers["Result"] = board.result()
            #print game


            print 'bestmove: ', handler.info["pv"][1][0]

            i = 0

            print 'pv: ', len(handler.info["pv"])
            max = len(handler.info["pv"][1])
            print 'depth: ', max

            testlist = []

            for x in range(0, max):
                testlist.append(handler.info["pv"][1][x])

            print 'testlist=', testlist


            # Add line:            
            if (handler.info["score"][1].cp is not None and str(handler.info["score"][2].cp/100.0) is not None):
                game.add_line(testlist, comment = str(handler.info["score"][1].cp/100.0) + " " + board.variation_san(handler.info["pv"][2]) + " " + str(handler.info["score"][2].cp/100.0) )
                game.promote_to_main(handler.info["pv"][1][0])
            

            game.headers["Result"] = board.result()
            print game

            if (handler.info["score"][2].cp is not None):
                node.add_variation(handler.info["pv"][2][0])
            
            print board
            print board.fen()
            print board.result()

            game.headers["Result"] = board.result()
            print game


            # Write the new PGN to the database, now

            new_pgn = open("test.pgn", "a")
            #new_pgn = open("test", "w")
            exporter = chess.pgn.FileExporter(new_pgn)
            game.accept(exporter)
            engine.quit()

            
            #break
        except ValueError:
            print "Ooops!"
        

