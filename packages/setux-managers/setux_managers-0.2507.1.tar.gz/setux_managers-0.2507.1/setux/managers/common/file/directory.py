from pathlib import Path

from pybrary.ascii import oct_mod

from setux.logger import debug, info, error
from setux.managers.common.file.common import PathChecker


ignore = 'verbose', 'sudo'


class Distro(PathChecker):
    '''Directories managment
    '''
    manager = 'dir'

    def do_validate(self, specs):
        for k, v in specs.items():
            if k == 'name':
                yield k, v
            elif k == 'mode':
                yield k, str(v) if v else None
            elif k == 'user':
                yield k, v
            elif k == 'group':
                yield k, v
            else:
                if k in ignore: continue
                debug(f'Invalid Spec for {self.manager} : {k}={v}')

    def get(self):
        ret, out, err = self.run(
            f'ls -ld --color=never {self.key}',
            report = 'quiet',
            check  = False,
        )
        if ret:
            debug(err)
            return
        try:
            mod, ln, usr, grp, size, month, day, time, path = out[0].split()
            typ, mod = mod[0], mod[1:10]
            assert typ=='d', f'DIR {self.key} : {typ} !'
            return dict(
                name  = path,
                mode  = oct_mod(mod),
                user  = usr,
                group = grp,
            )
        except Exception as x:
            debug('dir %s !\n%s : %s', self.key, type(x), x)

    def cre(self):
        if not self.quiet:
            debug(f'dir create {self.key}')
        parent = Path(self.key).parent
        ret, out, err = self.run(
            f'ls -d {parent}',
            report = 'quiet',
            check  = False,
        )
        if ret:
            spec = dict(self.spec)
            spec['verbose'] = False
            Distro(
                self.distro, quiet=True
            )(
                parent, **spec
            )
            ret, out, err = self.run(f'mkdir -p {self.key}')


    def mod(self, key, val):
        debug(f'dir {self.key} change {key} -> {val}')
        if key=='mode':
            self.run(f'chmod -R {val} {self.key}')
        elif (
            key in ('user', 'group')
            and 'user' in self.spec
            and 'group' in self.spec
        ):
            usr = self.spec["user"]
            grp = self.spec["group"]
            self.run(f'chown -R {usr}:{grp} {self.key}')
        elif key=='user':
            self.run(f'chown -R {val} {self.key}')
        elif key=='group':
            self.run(f'chgrp -R {val} {self.key}')
        else:
            raise KeyError(f' ! {key} !')

    def rm(self, check=True):
        if self.get():
            debug(f'dir delete {self.key}')
            report = 'normal' if check else 'quiet'
            self.run(
                f'rm -rf {self.key}',
                check = check,
                report = report,
            )

    @property
    def hash(self):
        hasher = 'shasum -b'
        hcmd = f'find {self.key} -type f -print0 | xargs -0 {hasher} | cut -b-40 | sort | {hasher}'
        ret, out, err =  self.run(hcmd, report='quiet')
        if ret: return None
        h, _p = out[0].split()
        return h

    def __str__(self):
        data = self.get()
        if data:
            return f'Dir {self.key} {data["mode"]} {data["user"]}:{data["group"]}'
        else:
            return f'Dir {self.key} not found'

