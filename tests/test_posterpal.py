import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from posterpal import process_files, load_config, clear_directory
import shutil
import filecmp

predicate = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_teds():
    """Tests a condition where two similar titles would overwrite the other due to race cases."""

    test_config = load_config(predicate + "/tests/test_config.json")

    # Ensure test directories are cleared even if failure prior
    clear_directory(predicate + "/tests/shows/Ted Lasso")
    clear_directory(predicate + "/tests/movies/Ted (2012)")
    clear_directory(predicate + "/tests/backup")

    for i in range(10): # Was successful at 50 but reduced for time
        # Move zip files to copy
        shutil.copy2(predicate + "/tests/zips/Ted Tests.zip", predicate + "/tests/process/Ted Tests.zip")
        shutil.copy2(predicate + "/tests/zips/Ted Lasso Tests.zip", predicate + "/tests/process/Ted Lasso Tests.zip")
        
        # Run primary function in posterpal
        process_files(test_config)
        
        # Check that files are in correct places
        assert filecmp.cmp(predicate + "/tests/verification/Ted.jpg", predicate + "/tests/movies/Ted (2012)/poster.jpg")
        assert filecmp.cmp(predicate + "/tests/verification/TedLasso.jpg", predicate + "/tests/shows/Ted Lasso/poster.jpg")

        # Clear folders for next run
        clear_directory(predicate + "/tests/shows/Ted Lasso")
        clear_directory(predicate + "/tests/movies/Ted (2012)")
        clear_directory(predicate + "/tests/backup")
