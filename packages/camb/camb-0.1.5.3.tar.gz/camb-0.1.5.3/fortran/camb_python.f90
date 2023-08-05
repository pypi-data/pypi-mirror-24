    module handles
    use CAMB
    use Precision
    use ModelParams
    use Transfer
    use iso_c_binding
    implicit none

    Type c_MatterTransferData
        integer   ::  num_q_trans   !    number of steps in k for transfer calculation
        type(c_ptr) :: q_trans, sigma_8, sigma2_vdelta_8, TransferData
        integer :: sigma_8_size(2)
        integer :: sigma2_vdelta_8_size(2)
        integer :: TransferData_size(3)
    end Type c_MatterTransferData


    Type c_ClTransferData
        integer :: NumSources
        integer :: q_size
        type(c_ptr) :: q
        integer delta_size(3)
        type(c_ptr) Delta_p_l_k
        integer l_size
        type(c_ptr) ls
        !skip limber for now...
    end Type c_ClTransferData

    contains

    !SPECIAL BRIDGE ROUTINES FOR PYTHONset

    subroutine CAMBdata_new(handle)
    type(c_ptr), intent(out) :: handle
    Type (CAMBdata), pointer :: pCAMBdata

    allocate(pCAMBdata)
    call CAMB_InitCAMBdata(pCAMBdata)
    call CAMB_setDefParams(pCAMBdata%Params)
    handle = c_loc(pCAMBdata)

    end subroutine CAMBdata_new

    subroutine CAMBdata_free(cptr)
    type(c_ptr)  :: cptr
    Type (CAMBdata), pointer :: pCAMBdata

    call c_f_pointer(cptr, pCAMBdata)
    call CAMB_FreeCAMBdata(pCAMBdata)
    deallocate(pCAMBdata)

    end subroutine CAMBdata_free

    subroutine CAMBdata_setParams(data, Params)
    Type (CAMBdata), target :: data
    type(CAMBparams) :: Params

    data%Params = Params

    end subroutine CAMBdata_setParams

    subroutine CAMBdata_getParams(data, handle)
    Type (CAMBdata), target :: data
    type(c_ptr), intent(out)  ::  handle

    handle = c_loc(data%Params)

    end subroutine CAMBdata_getParams

    function CAMBdata_GetTransfers(data, Params, onlytransfer) result(error)
    Type (CAMBdata):: data
    type(CAMBparams) :: Params, P
    logical(kind=c_bool)  :: onlytransfer
    integer :: error

    P = Params
    if (P%DoLensing .and. (P%NonLinear == NonLinear_lens .or. P%NonLinear == NonLinear_both)) then
        P%WantTransfer = .true.
        call Transfer_SetForNonlinearLensing(P%Transfer)
    end if
    call Transfer_SortAndIndexRedshifts(P%Transfer)
    error = 0

    P%OnlyTransfers = onlytransfer
    call CAMB_GetTransfers(P, data, error)

    end function CAMBdata_GetTransfers

    subroutine CAMBdata_SetParamsForBackground(data, P)
    Type (CAMBdata):: data
    type(CAMBparams) :: P

    global_error_flag = 0
    data%Params = P
    call CAMBParams_Set(data%Params)
    end subroutine CAMBdata_SetParamsForBackground

    function CAMBdata_CalcBackgroundTheory(data, P) result(error)
    use cambmain, only: initvars
    Type (CAMBdata):: data
    type(CAMBparams) :: P
    integer error

    global_error_flag = 0
    data%Params = P
    call CAMBParams_Set(data%Params)
    call InitVars !calculate thermal history, e.g. z_drag etc.
    error=global_error_flag

    end function CAMBdata_CalcBackgroundTheory


    subroutine CAMBdata_MatterTransferData(data, cData)
    Type(CAMBdata), target :: data
    Type(c_MatterTransferData) :: cData

    cData%num_q_trans = data%MTrans%num_q_trans
    cData%q_trans = c_loc(data%MTrans%q_trans)
    cData%sigma_8 = c_loc(data%MTrans%sigma_8)
    cData%sigma2_vdelta_8 = c_loc(data%MTrans%sigma2_vdelta_8)
    cData%TransferData = c_loc(data%MTrans%TransferData)
    cData%q_trans = c_loc(data%MTrans%q_trans)
    cData%sigma_8_size = shape(data%MTrans%sigma_8)
    cData%sigma2_vdelta_8_size = shape(data%MTrans%sigma2_vdelta_8)
    cData%TransferData_size = shape(data%MTrans%TransferData)

    end subroutine CAMBdata_MatterTransferData

    subroutine CAMBdata_ClTransferData(data, cData, i)
    Type(CAMBdata), target :: data
    Type(c_ClTransferData) :: cData
    integer, intent(in) :: i

    if (i==0) then
        call Convert_ClTransferData(data%ClTransScal, cData)
    else if (i==1) then
        call Convert_ClTransferData(data%ClTransVec, cData)
    else if (i==2) then
        call Convert_ClTransferData(data%ClTransTens, cData)
    else
        error stop 'Unknown ClTransferData index'
    end if

    end subroutine CAMBdata_ClTransferData

    subroutine Convert_ClTransferData(data, cData)
    Type(ClTransferData), target :: data
    Type(c_ClTransferData) :: cData

    cData%NumSources = data%NumSources
    if (associated(Data%q%points)) then
        cData%q_size = size(data%q%points)
        cData%q = c_loc(data%q%points)
    else
        cData%q_size = 0
    end if
    if (associated(data%Delta_p_l_k)) then
        cData%delta_size = shape(Data%Delta_p_l_k)
        cData%delta_p_l_k = c_loc(Data%Delta_p_l_k)
    else
        cData%delta_size = 0
    end if
    cdata%l_size = Data%ls%l0
    cdata%ls = c_loc(Data%ls%l)

    end subroutine Convert_ClTransferData


    subroutine CAMBdata_GetLinearMatterPower(data, PK, var1, var2, hubble_units)
    Type(CAMBdata) :: data
    real(dl) :: PK(data%MTrans%num_q_trans,data%Params%Transfer%PK_num_redshifts)
    integer, intent(in) :: var1, var2
    logical :: hubble_units

    call Transfer_GetUnsplinedPower(data%MTrans, PK, var1, var2, hubble_units)

    end subroutine CAMBdata_GetLinearMatterPower

    subroutine CAMBdata_GetNonLinearMatterPower(data, PK, var1, var2, hubble_units)
    Type(CAMBdata) :: data
    real(dl) :: PK(data%MTrans%num_q_trans,data%Params%Transfer%PK_num_redshifts)
    integer, intent(in) :: var1, var2
    logical :: hubble_units

    call Transfer_GetUnsplinedNonlinearPower(data%MTrans, PK, var1, var2, hubble_units)

    end subroutine CAMBdata_GetNonLinearMatterPower


    subroutine CAMBdata_GetMatterPower(data, outpower, minkh, dlnkh, npoints, var1, var2)
    Type(CAMBdata) :: data
    real(dl), intent(out) :: outpower(npoints,data%Params%Transfer%PK_num_redshifts)
    real(dl), intent(in) :: minkh, dlnkh
    integer, intent(in) :: npoints, var1, var2
    integer i

    do i=1,data%Params%Transfer%PK_num_redshifts
        call Transfer_GetMatterPowerD(data%MTrans,outpower(:,i), data%Params%Transfer%PK_num_redshifts-i+1, &
            & 1, minkh, dlnkh, npoints, var1, var2)
    end do

    end subroutine CAMBdata_GetMatterPower


    subroutine CAMB_setinitialpower(Params, P)
    type(CAMBparams) :: Params
    type(InitialPowerParams) :: P

    Params%InitPower = P

    end subroutine CAMB_setinitialpower


    subroutine CAMB_SetTotCls(lmax, tot_scalar_Cls, in)
    integer, intent(IN) :: lmax, in
    real(dl), intent(OUT) :: tot_scalar_cls(4, 0:lmax)
    integer l

    tot_scalar_cls = 0
    do l=lmin, lmax
        if (CP%WantScalars .and. l<= CP%Max_l) then
            if (CP%DoLensing) then
                if (l<=lmax_lensed) tot_scalar_cls(1:4,l) = Cl_lensed(l, in, CT_Temp:CT_Cross)
            else
                tot_scalar_cls(1:2,l) = Cl_scalar(l, in,  C_Temp:C_E)
                tot_scalar_cls(4,l) = Cl_scalar(l, in,  C_Cross)
            endif
        end if
        if (CP%WantTensors .and. l <= CP%Max_l_tensor) then
            tot_scalar_cls(1:4,l) = tot_scalar_cls(1:4,l) + Cl_tensor(l, in,  CT_Temp:CT_Cross)
        end if
    end do

    end subroutine CAMB_SetTotCls

    subroutine CAMB_SetUnlensedCls(lmax, unlensed_cls, in)
    integer, intent(IN) :: lmax, in
    real(dl), intent(OUT) :: unlensed_cls(4,0:lmax)
    integer l

    unlensed_cls = 0
    do l=lmin, lmax
        if (CP%WantScalars .and. l<= CP%Max_l) then
            unlensed_cls(1:2,l) = Cl_scalar(l, in,  C_Temp:C_E)
            unlensed_cls(4,l) = Cl_scalar(l, in,  C_Cross)
        end if
        if (CP%WantTensors .and. l <= CP%Max_l_tensor) then
            unlensed_cls(1:4,l) = unlensed_cls(1:4,l) + Cl_tensor(l, in,  CT_Temp:CT_Cross)
        end if
    end do

    end subroutine CAMB_SetUnlensedCls

    subroutine CAMB_SetLensPotentialCls(lmax, cls, in)
    use constants
    integer, intent(IN) :: lmax, in
    real(dl), intent(OUT) :: cls(3, 0:lmax) !phi-phi, phi-T, phi-E
    integer l

    cls = 0
    if (CP%WantScalars .and. CP%DoLensing) then
        do l=lmin, min(lmax,CP%Max_l)
            cls(1,l) = Cl_scalar(l,in,C_Phi) * (real(l+1)/l)**2/const_twopi
            cls(2:3,l) = Cl_scalar(l,in,C_PhiTemp:C_PhiE) * ((real(l+1)/l)**1.5/const_twopi)
        end do
    end if

    end subroutine CAMB_SetLensPotentialCls

    subroutine CAMB_SetUnlensedScalCls(lmax, scalar_Cls, in)
    integer, intent(IN) :: lmax, in
    real(dl), intent(OUT) :: scalar_Cls(4, 0:lmax)
    integer lmx

    scalar_Cls = 0
    if (CP%WantScalars) then
        lmx = min(CP%Max_l, lmax)
        scalar_Cls(1:2,lmin:lmx) = transpose(Cl_Scalar(lmin:lmx, in,C_Temp:C_E))
        scalar_Cls(4,lmin:lmx) = Cl_Scalar(lmin:lmx, in,C_Cross)
    end if

    end subroutine CAMB_SetUnlensedScalCls

    subroutine CAMB_SetlensedScalCls(lmax, lensed_Cls, in)
    integer, intent(IN) :: lmax, in
    real(dl), intent(OUT) :: lensed_Cls(4, 0:lmax)
    integer lmx

    lensed_Cls = 0
    if (CP%WantScalars .and. CP%DoLensing) then
        lmx = min(lmax,lmax_lensed)
        lensed_Cls(1:4,lmin:lmx) = transpose(Cl_lensed(lmin:lmx, in,CT_Temp:CT_Cross))
    end if

    end subroutine CAMB_SetlensedScalCls

    subroutine CAMB_SetTensorCls(lmax, tensor_Cls, in)
    integer, intent(IN) :: lmax, in
    real(dl), intent(OUT) :: tensor_Cls(4, 0:lmax)
    integer lmx

    tensor_Cls = 0
    if (CP%WantTensors) then
        lmx = min(lmax,CP%Max_l_tensor)
        tensor_Cls(1:3,lmin:lmx) = transpose(Cl_Tensor(lmin:lmx, in, CT_Temp:CT_Cross))
    end if

    end subroutine CAMB_SetTensorCls


    subroutine CAMB_SetUnlensedScalarArray(lmax, ScalarArray, in, n)
    integer, intent(IN) :: lmax, in, n
    real(dl), intent(OUT) :: ScalarArray(n, n, 0:lmax)
    integer l

    ScalarArray = 0
    if (CP%WantScalars) then
        do l=lmin, min(lmax,CP%Max_l)
            ScalarArray(1:n,1:n,l) = Cl_scalar_array(l, in, 1:n,1:n)
        end do
    end if

    end subroutine CAMB_SetUnlensedScalarArray

    subroutine CAMB_SetBackgroundOutputs_z(redshifts,n)
    integer, intent(in) :: n
    real(dl), intent(in) :: redshifts(n)

    if (associated(BackgroundOutputs%z_outputs)) deallocate(BackgroundOutputs%z_outputs)
    if (n>0) then
        allocate(BackgroundOutputs%z_outputs(n))
        BackgroundOutputs%z_outputs = redshifts
    else
        nullify(BackgroundOutputs%z_outputs)
    end if

    end subroutine CAMB_SetBackgroundOutputs_z

    function CAMB_GetNumBackgroundOutputs()
    integer CAMB_GetNumBackgroundOutputs

    if (.not. associated(BackgroundOutputs%z_outputs)) then
        CAMB_GetNumBackgroundOutputs = 0
    else
        CAMB_GetNumBackgroundOutputs = size(BackgroundOutputs%z_outputs)
    end if

    end function CAMB_GetNumBackgroundOutputs

    subroutine CAMB_GetBackgroundOutputs(outputs, n)
    use constants
    integer, intent(in) :: n
    real(dl), intent(out) :: outputs(4,n)
    integer i

    if (associated(BackgroundOutputs%z_outputs)) then
        do i=1, size(BackgroundOutputs%z_outputs)
            outputs(1,i) = BackgroundOutputs%rs_by_D_v(i)
            outputs(2,i) = BackgroundOutputs%H(i)*c/1e3_dl
            outputs(3,i) = BackgroundOutputs%DA(i)
            outputs(4,i) = (1+BackgroundOutputs%z_outputs(i))* &
                BackgroundOutputs%DA(i) * BackgroundOutputs%H(i) !F_AP parameter
        end do
    end if

    end subroutine CAMB_GetBackgroundOutputs


    subroutine set_cls_template(cls_template)
    character(len=*), intent(in) :: cls_template

    highL_unlensed_cl_template = trim(cls_template)

    end subroutine set_cls_template

    function CAMB_PrimordialPower(Params, k, powers, n,  i) result(err)
    use constants
    type(CAMBparams) :: Params
    integer, intent(in) :: i,n
    real(dl), intent(in) :: k(n)
    real(dl), intent(out) :: powers(n)
    real(dl) curv
    integer err,ix

    global_error_flag = 0
    curv =-Params%omegak/((c/1000)/Params%h0)**2
    call InitializePowers(Params%InitPower,curv)
    if (global_error_flag==0) then
        do ix =1, n
            if (i==0) then
                powers(ix) = ScalarPower(k(ix),1)
            elseif (i==2) then
                powers(ix) = TensorPower(k(ix),1)
            else
                error stop 'Unknown power type index'
            end if
            if (global_error_flag /= 0) exit
        end do
    end if
    err= global_error_flag

    end function CAMB_PrimordialPower

    subroutine GetOutputEvolutionFork(EV, times, outputs)
    use Transfer
    use CAMBmain
    implicit none
    type(EvolutionVars) EV
    real(dl), intent(in) :: times(:)
    real(dl), intent(out) :: outputs(:,:,:)
    real(dl) tau,tol1,tauend, taustart
    integer j,ind,itf
    real(dl) c(24),w(EV%nvar,9), y(EV%nvar)
    real(dl) yprime(EV%nvar), ddelta, delta, adotoa,dtauda, growth, x_e, a, x_e_recomb
    external dtauda
    real, target :: Arr(Transfer_max)

    w=0
    y=0
    taustart = GetTauStart(min(500._dl,EV%q))
    call initial(EV,y, taustart)

    tau=taustart
    ind=1
    tol1=tol/exp(AccuracyBoost-1)
    do j=1,size(times)
        tauend = times(j)
        if (tauend<taustart) cycle

        call GaugeInterface_EvolveScal(EV,tau,y,tauend,tol1,ind,c,w)
        yprime = 0
        EV%OutputTransfer =>  Arr
        call derivs(EV,EV%ScalEqsToPropagate,tau,y,yprime)
        nullify(EV%OutputTransfer)
        a = y(1)
        outputs(1:Transfer_Max, j, EV%q_ix) = Arr
        outputs(Transfer_Max+1, j, EV%q_ix) = a
        outputs(Transfer_Max+2, j, EV%q_ix) = y(2) !etak
        adotoa = 1/(y(1)*dtauda(y(1)))
        ddelta= (yprime(3)*grhoc+yprime(4)*grhob)/(grhob+grhoc)
        delta=(grhoc*y(3)+grhob*y(4))/(grhob+grhoc)
        growth= ddelta/delta/adotoa
        outputs(Transfer_Max+3, j, EV%q_ix) = adotoa !hubble
        outputs(Transfer_Max+4, j, EV%q_ix) = growth
        if (.not. EV%no_phot_multpoles) then
            outputs(Transfer_Max+5, j, EV%q_ix) = y(EV%g_ix+1) !v_g
            if (EV%TightCoupling) then
                outputs(Transfer_Max+6, j, EV%q_ix) = EV%pig
                outputs(Transfer_Max+7, j, EV%q_ix) = EV%pig/4 !just first order result
            else
                outputs(Transfer_Max+6, j, EV%q_ix) = y(EV%g_ix+2) !pi_g
                outputs(Transfer_Max+7, j, EV%q_ix) = y(EV%polind+2) !E_2
            end if
        end if
        if (.not. EV%no_nu_multpoles) then
            outputs(Transfer_Max+8, j, EV%q_ix) = y(EV%r_ix+1) !v_r
        end if

        if (global_error_flag/=0) return
    end do
    end subroutine GetOutputEvolutionFork

    function CAMB_TimeEvolution(nq, q, ntimes, times, noutputs, outputs) result(err)
    integer, intent(in) :: nq, ntimes, noutputs
    real(dl), intent(in) :: q(nq), times(ntimes)
    real(dl), intent(out) :: outputs(Transfer_Max+8, ntimes, nq)
    integer err
    integer q_ix
    Type(EvolutionVars) :: Ev

    global_error_flag = 0
    outputs = 0
    !$OMP PARALLEL DO DEFAUlT(SHARED),SCHEDUlE(DYNAMIC), PRIVATE(EV, q_ix)
    do q_ix= 1, nq
        if (global_error_flag==0) then
            EV%q_ix = q_ix
            EV%q = q(q_ix)
            EV%TransferOnly=.false.
            EV%q2=EV%q**2
            call GetNumEqns(EV)
            call GetOutputEvolutionFork(EV, times, outputs)
        end if
    end do
    !$OMP END PARALLEL DO
    err = global_error_flag
    end function CAMB_TimeEvolution

    ! END BRIDGE FOR PYTHON

    end module handles
