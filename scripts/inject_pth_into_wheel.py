"""Inject ibm_db_dll.pth into a wheel so it lands in site-packages on install.

Usage: python scripts/inject_pth_into_wheel.py <wheel_dir>

Wheels are zip files. Files at the root level of a wheel (alongside .py
modules) are installed to site-packages. This script adds ibm_db_dll.pth
to every .whl file in the given directory.
"""
import os, sys, hashlib, base64, zipfile, glob, tempfile, shutil

PTH_FILENAME = 'ibm_db_dll.pth'
PTH_CONTENT = 'import _ibm_db_register_dll\n'


def _record_line(name, content_bytes):
    """Build a RECORD entry: name,sha256=<digest>,<length>"""
    digest = hashlib.sha256(content_bytes).digest()
    b64 = base64.urlsafe_b64encode(digest).rstrip(b'=').decode('ascii')
    return f'{name},sha256={b64},{len(content_bytes)}'


def inject_pth(whl_path):
    """Add ibm_db_dll.pth to a wheel file and remove any misplaced copies."""
    with zipfile.ZipFile(whl_path, 'r') as zin:
        names = zin.namelist()
        # Skip if the .pth file is already at the wheel root
        if PTH_FILENAME in names:
            print(f'  {PTH_FILENAME} already at root of {os.path.basename(whl_path)}, skipping')
            return

    tmp_fd, tmp_path = tempfile.mkstemp(suffix='.whl')
    os.close(tmp_fd)

    pth_bytes = PTH_CONTENT.encode('utf-8')
    pth_record = _record_line(PTH_FILENAME, pth_bytes)

    with zipfile.ZipFile(whl_path, 'r') as zin, \
         zipfile.ZipFile(tmp_path, 'w', zipfile.ZIP_DEFLATED) as zout:

        for item in zin.infolist():
            # Drop any misplaced copies of the .pth file (absolute-path junk from data_files)
            if item.filename != PTH_FILENAME and item.filename.endswith('/' + PTH_FILENAME):
                print(f'  Removing misplaced {item.filename}')
                continue

            data = zin.read(item.filename)

            # Append our .pth entry to the RECORD file
            if item.filename.endswith('/RECORD'):
                data = data.rstrip(b'\n') + b'\n' + pth_record.encode('utf-8') + b'\n'

            zout.writestr(item, data)

        # Add the .pth file at the wheel root
        zout.writestr(PTH_FILENAME, pth_bytes)

    shutil.move(tmp_path, whl_path)
    print(f'  Injected {PTH_FILENAME} into {os.path.basename(whl_path)}')


def main():
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <wheel_dir>')
        sys.exit(1)

    wheel_dir = sys.argv[1]
    wheels = glob.glob(os.path.join(wheel_dir, '*.whl'))

    if not wheels:
        print(f'No .whl files found in {wheel_dir}')
        sys.exit(1)

    for whl in wheels:
        inject_pth(whl)

    print(f'Done: processed {len(wheels)} wheel(s)')


if __name__ == '__main__':
    main()
