import os
import sys
import winreg  

def add_to_path(new_paths):
    try:
        
        current_path = os.environ.get('PATH', '')

        
        new_path = os.pathsep.join(new_paths) + os.pathsep + current_path
        
       
        os.environ['PATH'] = new_path

        
        if sys.platform == 'win32':
            key = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
            value = 'PATH'
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, value, 0, winreg.REG_EXPAND_SZ, new_path)
            
            print("PATH updated successfully. You may need to restart your command prompt.")
        else:
            print("This script is intended to run on Windows only.")
    except Exception as e:
        print(f"Failed to update PATH: {e}")

def main():
    
    new_paths = [
        r"E:\satony",
    ]
    add_to_path(new_paths)
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
