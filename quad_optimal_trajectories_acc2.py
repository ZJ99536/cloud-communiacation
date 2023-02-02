from casadi import MX, DM, vertcat, horzcat, veccat, norm_2, dot, mtimes, nlpsol, diag, repmat, sum1, sin, cos, tan
import casadi as ca
# from cv2 import sqrt
import numpy as np
# from pygments import lex
import matplotlib.pyplot as plt



class Planner:
    def __init__(self,wpx,wpy,wpz):
        ## changeable
        
        self.NX = 1
        # self.a_max = 5
        # self.wpx = [4.0, 4.5]
        # self.wpy = [8.0, 7.5]
        # self.wpz = [3.0, 6.0]
        self.wpx = wpx
        self.wpy = wpy
        self.wpz = wpz
        # self.wpx = [0.0]
        # self.wpy = [4.0]
        # self.wpz = [2.0]
        self.vel_guess = 3.0
        self.tol = 0.2
        self.gravity = 9.81
        self.m = 1
        self.l = 1
        ## self.I
        self.ctau = 0.5
        self.T_max = 3.6
        self.T_min = 0

        self.NW = len(self.wpx)
        self.dis = ((self.wpx[0])**2 + (self.wpy[0])**2 + (self.wpz[0]-2.0)**2)**0.5
        for i in range(len(self.wpx)-1):
            self.dis += ((self.wpx[i+1]-self.wpx[i])**2 + (self.wpy[i+1]-self.wpy[i])**2 + (self.wpz[i+1]-self.wpz[i])**2)**0.5
        self.N = int(self.dis / 0.04)
        print(self.N)

        if self.dis / self.N < self.tol:
            print("sufficient")
            print("sufficient")
            print("sufficient")
            print("sufficient")
            print("sufficient")
            print("sufficient")
        else:
            print("insufficient")
            print("insufficient")
            print("insufficient")
            print("insufficient")
            print("insufficient")

        # Problem variables
        self.x = []
        self.xg = []
        self.g = []
        self.lb = []
        self.ub = []
        self.J = []

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
            x += [self.lamx]
            xg += [1]*self.NW
            g += [self.lamx]
            lb += [0]*self.NW
            ub += [1]*self.NW
            
            self.accx = MX.sym('accx' + str(i), self.NX)
            self.accy = MX.sym('accy' + str(i), self.NX)
            self.accz = MX.sym('accz' + str(i), self.NX)
            x += [self.accx]
            xg += [0]
            x += [self.accy]
            xg += [0]
            x += [self.accz]
            xg += [0]
            
            self.mux = MX.sym('mu' + str(i), self.NW)
            
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
        # g += [ax_end]
        # lb += [0]
        # ub += [0]
        ay_end = MX.sym('ay_end', self.NX)
        x += [ay_end]
        xg += [0]
        # g += [ay_end]
        # lb += [0]
        # ub += [0]
        az_end = MX.sym('az_end', self.NX)
        x += [az_end]
        xg += [0]
        # g += [az_end]
        # lb += [0]
        # ub += [0]
        wx_end = MX.sym('wx_end', self.NX)
        x += [wx_end]
        xg += [0]
        # g += [wx_end]
        # lb += [0]
        # ub += [0]
        wy_end = MX.sym('wy_end', self.NX)
        x += [wy_end]
        xg += [0]
        # g += [wy_end]
        # lb += [0]
        # ub += [0]
        wz_end = MX.sym('wz_end', self.NX)
        x += [wz_end]
        xg += [0]
        # g += [wz_end]
        # lb += [0]
        # ub += [0]

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
        # g += [accx_end]
        # lb += [0]
        # ub += [0]
        accy_end = MX.sym('accy_end', self.NX)
        x += [accy_end]
        xg += [0]
        # g += [accy_end]
        # lb += [0]
        # ub += [0]
        accz_end = MX.sym('accz_end', self.NX)
        x += [accz_end]
        xg += [0]
        # g += [accz_end]
        # lb += [0]
        # ub += [0]


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
    

if __name__ == "__main__":
    # plan = Planner()
    # # print(plan.solve())
    # x_sol, dt, N, NW = plan.solve()
    # print(x_sol[0])
    # t_x = ca.DM(np.linspace(0, x_sol[0], N+2, True))
    # s_x = []
    # s_y = []
    # s_z = []
    # v_x = []
    # v_y = []
    # v_z = []
    # u_1 = []
    # u_2 = []
    # u_3 = []
    # u_4 = []
    # u = []

    f = open("/root/cloud-communiacation/library/quad2.txt",'w')      

    wpx = [1,1]
    wpy = [1,1]
    wpz = [1,1]
    count = 0
    for x0i in range(-10,11):
        for x1i in range(0,1):
            for y0i in range(-10,11):
                for y1i in range(0,1):
                    for z0i in range(-10,11):
                        for z1i in range(0,1):
                            wpx[0] = 2.0 + x0i * 0.1
                            wpx[1] = 4.0 + x1i * 0.2
                            wpy[0] = 0.0 + y0i * 0.1
                            wpy[1] = 0.0 + y1i * 0.2
                            wpz[0] = 2.0 + z0i * 0.1
                            wpz[1] = 2.0 + z1i * 0.2

                            count += 1
                            print(count, "/ 9261")
                    
                            plan = Planner(wpx,wpy,wpz)
                            x_sol, dt, N, NW = plan.solve()
                            # print(x_sol[0])             
                            for i in range(N+1):                                
                                f.write(str(wpx[0]-x_sol[2+i*(3*NW + 20)])+',')
                                f.write(str(wpy[0]-x_sol[3+i*(3*NW + 20)])+',')
                                f.write(str(wpz[0]-x_sol[4+i*(3*NW + 20)])+',')
                                f.write(str(wpx[1]-x_sol[2+i*(3*NW + 20)])+',')
                                f.write(str(wpy[1]-x_sol[3+i*(3*NW + 20)])+',')
                                f.write(str(wpz[1]-x_sol[4+i*(3*NW + 20)])+',') 
                                f.write(str(x_sol[5+i*(3*NW + 20)])+',') #vx
                                f.write(str(x_sol[6+i*(3*NW + 20)])+',') #vy
                                f.write(str(x_sol[7+i*(3*NW + 20)])+',') #vz  
                                f.write(str(x_sol[20+i*(3*NW + 20)])+',') #ax
                                f.write(str(x_sol[21+i*(3*NW + 20)])+',') #ay
                                f.write(str(x_sol[22+i*(3*NW + 20)]+9.81)+',') #az
                                f.write(str(x_sol[11+i*(3*NW + 20)])+',') #wx
                                f.write(str(x_sol[12+i*(3*NW + 20)])+',') #wy
                                f.write(str(x_sol[13+i*(3*NW + 20)])+',') #wz
                                f.write(str(x_sol[14+i*(3*NW + 20)]+x_sol[15+i*(3*NW + 20)]+x_sol[16+i*(3*NW + 20)]+x_sol[17+i*(3*NW + 20)])+',')  
                                f.write(str(x_sol[18+i*(3*NW + 20)])+',')  
                                f.write(str(x_sol[19+i*(3*NW + 20)])+',')   

                                f.write(str(wpx[0]-x_sol[2+(i+1)*(3*NW + 20)])+',')
                                f.write(str(wpy[0]-x_sol[3+(i+1)*(3*NW + 20)])+',')
                                f.write(str(wpz[0]-x_sol[4+(i+1)*(3*NW + 20)])+',')
                                f.write(str(wpx[1]-x_sol[2+(i+1)*(3*NW + 20)])+',')
                                f.write(str(wpy[1]-x_sol[3+(i+1)*(3*NW + 20)])+',')
                                f.write(str(wpz[1]-x_sol[4+(i+1)*(3*NW + 20)])+',')
                                f.write(str(x_sol[5+(i+1)*(3*NW + 20)])+',') #vx
                                f.write(str(x_sol[6+(i+1)*(3*NW + 20)])+',') #vy
                                f.write(str(x_sol[7+(i+1)*(3*NW + 20)])+',') #vz  
                                f.write(str(x_sol[20+(i+1)*(3*NW + 20)])+',') #ax
                                f.write(str(x_sol[21+(i+1)*(3*NW + 20)])+',') #ay
                                f.write(str(x_sol[22+(i+1)*(3*NW + 20)]+9.81)+',') #az
                                f.write(str(x_sol[11+(i+1)*(3*NW + 20)])+',') #wx
                                f.write(str(x_sol[12+(i+1)*(3*NW + 20)])+',') #wy
                                f.write(str(x_sol[13+(i+1)*(3*NW + 20)])+',') #wz
                                f.write(str(x_sol[14+(i+1)*(3*NW + 20)]+x_sol[15+(i+1)*(3*NW + 20)]+x_sol[16+(i+1)*(3*NW + 20)]+x_sol[17+(i+1)*(3*NW + 20)])+',')  
                                f.write(str(x_sol[18+(i+1)*(3*NW + 20)])+',')  
                                f.write(str(x_sol[19+(i+1)*(3*NW + 20)])+',')
                                f.write(str(x_sol[8+(i+1)*(3*NW + 20)])+',') #qx
                                f.write(str(x_sol[9+(i+1)*(3*NW + 20)])+',') #qy
                                f.write(str(x_sol[10+(i+1)*(3*NW + 20)])+'\n') #qz
                                        
    f.close()
