import { ProductGrid } from "@/components/product-grid"

const products = [
  {
    id: 1,
    name: "Classic White T-Shirt",
    price: 29.99,
    image: "/placeholder.svg?height=400&width=300",
    category: "men",
    isNew: true,
  },
  {
    id: 2,
    name: "Slim Fit Jeans",
    price: 59.99,
    image: "/placeholder.svg?height=400&width=300",
    category: "men",
    isNew: false,
  },
  {
    id: 3,
    name: "Summer Floral Dress",
    price: 79.99,
    image: "/placeholder.svg?height=400&width=300",
    category: "women",
    isNew: true,
  },
  {
    id: 4,
    name: "Casual Hoodie",
    price: 49.99,
    image: "/placeholder.svg?height=400&width=300",
    category: "men",
    isNew: false,
  },
  {
    id: 5,
    name: "Denim Jacket",
    price: 89.99,
    image: "/placeholder.svg?height=400&width=300",
    category: "men",
    isNew: true,
  },
  {
    id: 6,
    name: "Pleated Skirt",
    price: 45.99,
    image: "/placeholder.svg?height=400&width=300",
    category: "women",
    isNew: false,
  },
  {
    id: 7,
    name: "Knit Sweater",
    price: 65.99,
    image: "/placeholder.svg?height=400&width=300",
    category: "women",
    isNew: true,
  },
  {
    id: 8,
    name: "Cargo Pants",
    price: 55.99,
    image: "/placeholder.svg?height=400&width=300",
    category: "men",
    isNew: false,
  },
]

export default function ProductsPage() {
  return (
    <div className="container px-4 py-12 mx-auto">
      <div className="flex flex-col items-center text-center space-y-2 mb-12">
        <h1 className="text-3xl font-bold tracking-tight">All Products</h1>
        <p className="text-muted-foreground max-w-[600px]">Browse our complete collection of premium clothing</p>
      </div>
      <ProductGrid products={products} />
    </div>
  )
}

