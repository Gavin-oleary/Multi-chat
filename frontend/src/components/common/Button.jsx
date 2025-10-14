const Button = ({ 
    children, 
    onClick, 
    variant = 'primary', 
    size = 'md',
    disabled = false,
    type = 'button',
    className = '',
    ...props
  }) => {
    const baseStyles = 'rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2'
    
    const variants = {
      primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500 disabled:bg-blue-300',
      secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500 disabled:bg-gray-100',
      danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500 disabled:bg-red-300',
      ghost: 'bg-transparent text-gray-700 hover:bg-gray-100 focus:ring-gray-500',
    }
    
    const sizes = {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-4 py-2 text-base',
      lg: 'px-6 py-3 text-lg',
    }
    
    return (
      <button
        type={type}
        onClick={onClick}
        disabled={disabled}
        className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className} ${
          disabled ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'
        }`}
        {...props}
      >
        {children}
      </button>
    )
  }
  
  export default Button