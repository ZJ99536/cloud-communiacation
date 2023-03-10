def solve(self):
        x = []
        xg = []
        g = []
        lb = []
        ub = []
        J = 0  
          
        t = MX.sym('t', 1)
        x += [t]
        xg += [self.dis/self.vel_guess]
        g += [t]
        lb += [0.1]
        ub += [150]
        J = t

        t_init = MX.sym('t_init', self.NX)
        x += [t_init]
        xg += [0]
        g += [t_init]
        lb += [0]
        ub += [0]

        x_init = MX.sym('x_init', self.NX)
        x += [x_init]
        xg += [0]
        g += [x_init]
        lb += [0]
        ub += [0]
        y_init = MX.sym('y_init', self.NX)
        x += [y_init]
        xg += [0]
        g += [y_init]
        lb += [0]
        ub += [0]
        z_init = MX.sym('z_init', self.NX)
        x += [z_init]
        xg += [2.0]
        g += [z_init]
        lb += [2.0]
        ub += [2.0]
        vx_init = MX.sym('vx_init', self.NX)
        x += [vx_init]
        xg += [0]
        g += [vx_init]
        lb += [0]
        ub += [0]
        vy_init = MX.sym('vy_init', self.NX)
        x += [vy_init]
        xg += [0]
        g += [vy_init]
        lb += [0]
        ub += [0]
        vz_init = MX.sym('vz_init', self.NX)
        x += [vz_init]
        xg += [0]
        g += [vz_init]
        lb += [0]
        ub += [0]

        ax_init = MX.sym('ax_init', self.NX)
        x += [ax_init]
        xg += [0]
        g += [ax_init]
        lb += [0]
        ub += [0]
        ay_init = MX.sym('ay_init', self.NX)
        x += [ay_init]
        xg += [0]
        g += [ay_init]
        lb += [0]
        ub += [0]
        az_init = MX.sym('az_init', self.NX)
        x += [az_init]
        xg += [0]
        g += [az_init]
        lb += [0]
        ub += [0]
        wx_init = MX.sym('wx_init', self.NX)
        x += [wx_init]
        xg += [0]
        g += [wx_init]
        lb += [0]
        ub += [0]
        wy_init = MX.sym('wy_init', self.NX)
        x += [wy_init]
        xg += [0]
        g += [wy_init]
        lb += [0]
        ub += [0]
        wz_init = MX.sym('wz_init', self.NX)
        x += [wz_init]
        xg += [0]
        g += [wz_init]
        lb += [0]
        ub += [0]

        u_init = MX.sym('u_init', 4)
        x += [u_init]
        xg += [self.m * self.gravity / 4] * 4
        g += [u_init]
        lb += [0] * 4
        ub += [self.T_max] * 4
        # ub += [self.m * self.gravity / 4 * 1.3] * 4

        lam_init = MX.sym('lam_init', self.NW)
        x += [lam_init]
        xg += [1]*self.NW
        g += [lam_init]
        lb += [1]*self.NW
        ub += [1]*self.NW
        mu_init = MX.sym('mu_init', self.NW)
        x += [mu_init]
        xg += [0]*self.NW
        g += [mu_init]
        lb += [0]*self.NW
        ub += [0]*self.NW
        tau = MX.sym('tau', self.NW)
        x += [tau]
        xg += [0] * self.NW
        g += [tau]
        lb += [0]*self.NW
        ub += [self.tol**2]*(self.NW)

        accx_init = MX.sym('accx_init', self.NX)
        x += [accx_init]
        xg += [0]
        g += [accx_init]
        lb += [0]
        ub += [0]
        accy_init = MX.sym('accy_init', self.NX)
        x += [accy_init]
        xg += [0]
        g += [accy_init]
        lb += [0]
        ub += [0]
        accz_init = MX.sym('accz_init', self.NX)
        x += [accz_init]
        xg += [0]
        g += [accz_init]
        lb += [0]
        ub += [0]

        dt = t / (self.N + 1)

        self.sx = x_init
        self.vx = vx_init
        self.sy = y_init
        self.vy = vy_init
        self.sz = z_init
        self.vz = vz_init

        self.ax = ax_init
        self.wx = wx_init
        self.ay = ay_init
        self.wy = wy_init
        self.az = az_init
        self.wz = wz_init

        self.u = u_init

        self.tx = t_init
        self.lamx = lam_init
        self.mux = mu_init

        self.accx = accx_init
        self.accy = accy_init
        self.accz = accz_init

        for i in range(self.N):
            lx = self.sx
            lvx = self.vx
            ly = self.sy
            lvy = self.vy
            lz = self.sz
            lvz = self.vz

            lax = self.ax
            lwx = self.wx
            lay = self.ay
            lwy = self.wy
            laz = self.az
            lwz = self.wz

            lu = self.u

            lt = self.tx
            llam = self.lamx
            lmu = self.mux

            laccx = self.accx
            laccy = self.accy
            laccz = self.accz

            self.tx = MX.sym('t'+str(i),1)
            x += [self.tx]
            xg += [0]
            g += [self.tx - lt - dt]
            lb += [0]
            ub += [0]            
            self.sx = MX.sym('sx' + str(i), self.NX)
            self.sy = MX.sym('sy' + str(i), self.NX)
            self.sz = MX.sym('sz' + str(i), self.NX)
            self.vx = MX.sym('vx' + str(i), self.NX)
            self.vy = MX.sym('vy' + str(i), self.NX)
            self.vz = MX.sym('vz' + str(i), self.NX)
            self.ax = MX.sym('ax' + str(i), self.NX)
            self.ay = MX.sym('ay' + str(i), self.NX)
            self.az = MX.sym('az' + str(i), self.NX)
            self.wx = MX.sym('wx' + str(i), self.NX)
            self.wy = MX.sym('wy' + str(i), self.NX)
            self.wz = MX.sym('wz' + str(i), self.NX)
            x += [self.sx]
            xg += [0]
            x += [self.sy]
            xg += [0]
            x += [self.sz]
            xg += [2.0]
            x += [self.vx]
            xg += [0]
            x += [self.vy]
            xg += [0]
            x += [self.vz]
            xg += [0]
            x += [self.ax]
            xg += [0]
            x += [self.ay]
            xg += [0]
            x += [self.az]
            xg += [0]
            x += [self.wx]
            xg += [0]
            x += [self.wy]
            xg += [0]
            x += [self.wz]
            xg += [0]

            self.u = MX.sym('u' + str(i), 4)
            x += [self.u]
            xg += [self.m * self.gravity / 4] * 4
            g += [self.u]
            lb += [0] * 4
            ub += [self.T_max] * 4
            # ub += [self.m * self.gravity / 4 * 1.3] * 4

            self.lamx = MX.sym('lam' + str(i), self.NW)
            self.mux = MX.sym('mu' + str(i), self.NW)
            x += [self.lamx]
            xg += [1]*self.NW
            g += [self.lamx]
            lb += [0]*self.NW
            ub += [1]*self.NW
            x += [self.mux]
            xg += [0]*self.NW
            g += [self.mux]
            lb += [0]*self.NW
            ub += [1]*self.NW
            tau = MX.sym('tau'+str(i), self.NW)
            x += [tau]
            xg += [0] * self.NW
            g += [tau]
            lb += [0]*self.NW
            ub += [self.tol**2]*(self.NW)

            self.accx = MX.sym('accx' + str(i), self.NX)
            self.accy = MX.sym('accy' + str(i), self.NX)
            self.accz = MX.sym('accz' + str(i), self.NX)
            x += [self.accx]
            xg += [0]
            x += [self.accy]
            xg += [0]
            x += [self.accz]
            xg += [0]

            for j in range(self.NW):
                diff = (self.sx - self.wpx[j])**2 + (self.sy - self.wpy[j])**2 + (self.sz - self.wpz[j])**2
                g += [self.mux[j] * (diff-tau[j])]
                lb += [0]
                ub += [0.01]

                if j < self.NW-1:
                    g += [self.lamx[j+1]-self.lamx[j]]
                    lb += [0]
                    ub += [1]
            
            g += [self.lamx - llam + lmu]
            lb += [0]*self.NW
            ub += [0]*self.NW

            ##x
            g += [(self.sx - lx) - lvx * dt]
            lb += [0]
            ub += [0]
            g += [(self.sy - ly) - lvy * dt]
            lb += [0]
            ub += [0]
            g += [(self.sz - lz) - lvz * dt]
            lb += [0]
            ub += [0]
            ##v
            phi = lax
            theta = lay
            psi = laz
            T = lu
            g += [(self.vx - lvx) - (cos(phi)*sin(theta)*cos(psi)+sin(phi)*sin(psi)) * (T[0]+T[1]+T[2]+T[3])/self.m * dt]
            lb += [0]
            ub += [0]
            g += [(self.vy - lvy) - (cos(phi)*sin(theta)*sin(psi)-sin(phi)*cos(psi)) * (T[0]+T[1]+T[2]+T[3])/self.m * dt]
            lb += [0]
            ub += [0]
            g += [(self.vz - lvz) - (cos(phi)*cos(theta) * (T[0]+T[1]+T[2]+T[3])/self.m - self.gravity) * dt]
            lb += [0]
            ub += [0]
            ##a
            g += [(self.ax - lax)-(lwx + tan(theta)*sin(phi)*lwy + tan(theta)*cos(phi)*lwz) * dt]
            lb += [0]
            ub += [0]
            g += [(self.ay - lay)-(cos(phi)*lwy - sin(phi)*lwz) * dt]
            lb += [0]
            ub += [0]
            g += [(self.az - laz)-(sin(phi)/cos(theta)*lwy + cos(phi)/cos(theta)*lwz) * dt]
            lb += [0]
            ub += [0]
            ##w
            g += [(self.wx - lwx)-(self.l/1.414*(T[0]-T[1]-T[2]+T[3]) - (-lwz*lwy + lwy*lwz)) * dt]
            lb += [0]
            ub += [0]
            g += [(self.wy - lwy)-(self.l/1.414*(-T[0]-T[1]+T[2]+T[3]) - (lwz*lwx - lwx*lwz)) * dt]
            lb += [0]
            ub += [0]
            g += [(self.wz - lwz)-(self.ctau*(T[0]-T[1]+T[2]-T[3]) - (-lwy*lwx + lwx*lwy)) * dt]
            lb += [0]
            ub += [0]

            #acc
            g += [(self.vx - lvx) - laccx * dt]
            lb += [0]
            ub += [0]
            g += [(self.vy - lvy) - laccy * dt]
            lb += [0]
            ub += [0]
            g += [(self.vz - lvz) - laccz * dt]
            lb += [0]
            ub += [0]

            g += [psi]
            lb += [-0.01]
            ub += [0.01]



        t_end = MX.sym('t_end', self.NX)
        x += [t_end]
        xg += [0]
        x_end = MX.sym('x_end', self.NX)
        x += [x_end]
        xg += [self.wpx[-1]]
        g += [x_end]
        lb += [self.wpx[-1]]
        ub += [self.wpx[-1]]
        y_end = MX.sym('y_end', self.NX)
        x += [y_end]
        xg += [self.wpy[-1]]
        g += [y_end]
        lb += [self.wpy[-1]]
        ub += [self.wpy[-1]]
        z_end = MX.sym('z_end', self.NX)
        x += [z_end]
        xg += [self.wpz[-1]]
        g += [z_end]
        lb += [self.wpz[-1]]
        ub += [self.wpz[-1]]
        vx_end = MX.sym('vx_end', self.NX)
        x += [vx_end]
        xg += [0]
        g += [vx_end]
        lb += [0]
        ub += [0]
        vy_end = MX.sym('vy_end', self.NX)
        x += [vy_end]
        xg += [0]
        g += [vy_end]
        lb += [0]
        ub += [0]
        vz_end = MX.sym('vz_end', self.NX)
        x += [vz_end]
        xg += [0]
        g += [vz_end]
        lb += [0]
        ub += [0]

        ax_end = MX.sym('ax_end', self.NX)
        x += [ax_end]
        xg += [0]
        g += [ax_end]
        lb += [0]
        ub += [0]
        ay_end = MX.sym('ay_end', self.NX)
        x += [ay_end]
        xg += [0]
        g += [ay_end]
        lb += [0]
        ub += [0]
        az_end = MX.sym('az_end', self.NX)
        x += [az_end]
        xg += [0]
        g += [az_end]
        lb += [0]
        ub += [0]
        wx_end = MX.sym('wx_end', self.NX)
        x += [wx_end]
        xg += [0]
        g += [wx_end]
        lb += [0]
        ub += [0]
        wy_end = MX.sym('wy_end', self.NX)
        x += [wy_end]
        xg += [0]
        g += [wy_end]
        lb += [0]
        ub += [0]
        wz_end = MX.sym('wz_end', self.NX)
        x += [wz_end]
        xg += [0]
        g += [wz_end]
        lb += [0]
        ub += [0]

        u_end = MX.sym('u_end', 4)
        x += [u_end]
        xg += [self.m * self.gravity / 4] * 4
        g += [u_end]
        lb += [self.m * self.gravity / 4] * 4
        ub += [self.m * self.gravity / 4] * 4


        lam_end = MX.sym('lam_end', self.NW)
        x += [lam_end]
        xg += [0]*self.NW
        g += [lam_end]
        lb += [0]*self.NW
        ub += [0]*self.NW

        accx_end = MX.sym('accx_end', self.NX)
        x += [accx_end]
        xg += [0]
        g += [accx_end]
        lb += [0]
        ub += [0]
        accy_end = MX.sym('accy_end', self.NX)
        x += [accy_end]
        xg += [0]
        g += [accy_end]
        lb += [0]
        ub += [0]
        accz_end = MX.sym('accz_end', self.NX)
        x += [accz_end]
        xg += [0]
        g += [accz_end]
        lb += [0]
        ub += [0]


        lx = self.sx
        lvx = self.vx
        ly = self.sy
        lvy = self.vy
        lz = self.sz
        lvz = self.vz

        lax = self.ax
        lwx = self.wx
        lay = self.ay
        lwy = self.wy
        laz = self.az
        lwz = self.wz

        lu = self.u

        lt = self.tx
        llam = self.lamx
        lmu = self.mux

        laccx = self.accx
        laccy = self.accy
        laccz = self.accz

        self.tx = t_end
        self.sx = x_end
        self.vx = vx_end
        self.sy = y_end
        self.vy = vy_end
        self.sz = z_end
        self.vz = vz_end

        self.ax = ax_end
        self.wx = wx_end
        self.ay = ay_end
        self.wy = wy_end
        self.az = az_end
        self.wz = wz_end

        self.lamx = lam_end
        g += [self.tx - lt - dt]
        lb += [0]
        ub += [0] 

        ##x
        g += [(self.sx - lx) - lvx * dt]
        lb += [0]
        ub += [0]
        g += [(self.sy - ly) - lvy * dt]
        lb += [0]
        ub += [0]
        g += [(self.sz - lz) - lvz * dt]
        lb += [0]
        ub += [0]
        ##v
        phi = lax
        theta = lay
        psi = laz
        T = lu
        g += [(self.vx - lvx) - (cos(phi)*sin(theta)*cos(psi)+sin(phi)*sin(psi)) * (T[0]+T[1]+T[2]+T[3])/self.m * dt]
        lb += [0]
        ub += [0]
        g += [(self.vy - lvy) - (cos(phi)*sin(theta)*sin(psi)-sin(phi)*cos(psi)) * (T[0]+T[1]+T[2]+T[3])/self.m * dt]
        lb += [0]
        ub += [0]
        g += [(self.vz - lvz) - (cos(phi)*cos(theta) * (T[0]+T[1]+T[2]+T[3])/self.m - self.gravity) * dt]
        lb += [0]
        ub += [0]
        ##a
        g += [(self.ax - lax)-(lwx + tan(theta)*sin(phi)*lwy + tan(theta)*cos(phi)*lwz) * dt]
        lb += [0]
        ub += [0]
        g += [(self.ay - lay)-(cos(phi)*lwy - sin(phi)*lwz) * dt]
        lb += [0]
        ub += [0]
        g += [(self.az - laz)-(sin(phi)/cos(theta)*lwy + cos(phi)/cos(theta)*lwz) * dt]
        lb += [0]
        ub += [0]
        ##w
        g += [(self.wx - lwx)-(self.l/1.414*(T[0]-T[1]-T[2]+T[3]) - (-lwz*lwy + lwy*lwz)) * dt]
        lb += [0]
        ub += [0]
        g += [(self.wy - lwy)-(self.l/1.414*(-T[0]-T[1]+T[2]+T[3]) - (lwz*lwx - lwx*lwz)) * dt]
        lb += [0]
        ub += [0]
        g += [(self.wz - lwz)-(self.ctau*(T[0]-T[1]+T[2]-T[3]) - (-lwy*lwx + lwx*lwy)) * dt]
        lb += [0]
        ub += [0]

        ##lam&mu
        g += [self.lamx - llam + lmu]
        lb += [0]*self.NW
        ub += [0]*self.NW

        #acc
        g += [(self.vx - lvx) - laccx * dt]
        lb += [0]
        ub += [0]
        g += [(self.vy - lvy) - laccy * dt]
        lb += [0]
        ub += [0]
        g += [(self.vz - lvz) - laccz * dt]
        lb += [0]
        ub += [0]

        # Reformat
        self.x = vertcat(*x)
        if not self.xg:
            self.xg = xg
        self.xg = veccat(*self.xg)
        self.g = vertcat(*g)
        self.lb = veccat(*lb)
        self.ub = veccat(*ub)
        self.J = J

        # Construct Non-Linear Program
        self.nlp = {'f': self.J, 'x': self.x, 'g': self.g}

        self.solver = nlpsol('solver', 'ipopt', self.nlp)
        self.solution = self.solver(x0=self.xg, lbg=self.lb, ubg=self.ub)
        self.x_sol = self.solution['x'].full().flatten()
        return self.x_sol, dt, self.N, self.NW