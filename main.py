from MainApp import MainApp
from dependencyinjection.di_container import DIContainer

if __name__ == "__main__":
    DIContainer.get_container()[MainApp].main()