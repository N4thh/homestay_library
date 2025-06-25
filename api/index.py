try:
    from pathlib import Path
    import sys
    sys.path.append(str(Path(__file__).resolve().parent.parent))

    from app import app
except Exception as e:
    import sys
    import traceback
    print('--- ERROR DURING APP IMPORT ---', file=sys.stderr)
    print(str(e), file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    app = None
    # Optionally, raise to force Vercel to show error
    raise

# Vercel sẽ tự động nhận biến app này 