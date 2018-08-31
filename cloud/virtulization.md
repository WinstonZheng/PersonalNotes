# 虚拟化
Hypervisor是用来控制虚拟机的程序。根据 Hypervisor的实现方式和所处的位置，虚拟化又分为两种：1型虚拟化和2型虚拟化。
- 1型虚拟化，Hypervisor 直接安装在物理机上，多个虚拟机在 Hypervisor 上运行。Hypervisor 实现方式一般是一个特殊定制的 Linux 系统。Xen 和 VMWare 的 ESXi 都属于这个类型；
- 2型虚拟化，物理机上首先安装常规的操作系统，比如 Redhat、Ubuntu 和 Windows。Hypervisor 作为 OS 上的一个程序模块运行，并对管理虚拟机进行管理。KVM、VirtualBox 和 VMWare Workstation 都属于这个类型。

比较：
- 1型虚拟化一般对硬件虚拟化功能进行了特别优化，性能上比2型要高；
- 2型虚拟化因为基于普通的操作系统，会比较灵活，比如支持虚拟机嵌套。嵌套意味着可以在KVM虚拟机中再运行KVM。

## KVM
KVM 全称是 Kernel-Based Virtual Machine。也就是说 KVM 是基于 Linux 内核实现的。KVM有一个内核模块叫 kvm.ko，只用于管理虚拟 CPU 和内存。那 IO 的虚拟化，比如存储和网络设备由谁实现呢？作为一个 Hypervisor，KVM 本身只关注虚拟机调度和内存管理这两个方面。IO 外设的任务交给 Linux 内核和 Qemu。

### Libvirt
Libvirt 除了能管理 KVM 这种 Hypervisor，还能管理 Xen，VirtualBox 等。OpenStack 底层也使用 Libvirt。Libvirt 包含 3 个东西：后台 daemon 程序 libvirtd、API 库和命令行工具 virsh
libvirtd是服务程序，接收和处理 API 请求；
API 库使得其他人可以开发基于 Libvirt 的高级工具，比如 virt-manager，这是个图形化的 KVM 管理工具，后面我们也会介绍；

### CPU虚拟化
KVM的虚拟化由CPU硬件支持，一个 KVM 虚机在宿主机中其实是一个 qemu-kvm 进程，与其他 Linux 进程一样被调度，虚机中的每一个虚拟 vCPU 则对应 qemu-kvm 进程中的一个线程。（虚机的 vCPU 总数可以超过物理 CPU 数量，这个叫 CPU overcommit（超配））

### 内存虚拟化
KVM 需要实现 VA（虚拟内存） -> PA（物理内存） -> MA（机器内存）之间的地址转换。虚机 OS 控制虚拟地址到客户内存物理地址的映射 （VA -> PA），但是虚机 OS 不能直接访问实际机器内存，因此 KVM 需要负责映射客户物理内存到实际机器内存 （PA -> MA）。

### 存储虚拟化
