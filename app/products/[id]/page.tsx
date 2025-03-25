"use client"

import { useState } from "react"
import Image from "next/image"
import Link from "next/link"
import { ChevronRight, Minus, Plus, ShoppingCart } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useCart } from "@/components/cart-provider"

// Mock product data - in a real app, you would fetch this from an API
const products = [
  {
    id: 1,
    name: "Classic White T-Shirt",
    price: 29.99,
    image: "/placeholder.svg?height=600&width=600",
    category: "men",
    isNew: true,
    description:
      "A timeless classic white t-shirt made from 100% organic cotton. Features a comfortable fit and durable construction that will last through countless washes.",
    details: {
      material: "100% Organic Cotton",
      fit: "Regular",
      care: "Machine wash cold, tumble dry low",
      origin: "Ethically made in Portugal",
    },
    sizes: ["XS", "S", "M", "L", "XL"],
    colors: ["White", "Black", "Gray"],
    images: [
      "/placeholder.svg?height=600&width=600",
      "/placeholder.svg?height=600&width=600",
      "/placeholder.svg?height=600&width=600",
    ],
  },
  {
    id: 2,
    name: "Slim Fit Jeans",
    price: 59.99,
    image: "/placeholder.svg?height=600&width=600",
    category: "men",
    isNew: false,
    description:
      "Modern slim fit jeans with a slight stretch for comfort. Features a classic five-pocket design and a versatile mid-wash that pairs well with anything.",
    details: {
      material: "98% Cotton, 2% Elastane",
      fit: "Slim",
      care: "Machine wash cold, inside out",
      origin: "Made in Turkey",
    },
    sizes: ["28", "30", "32", "34", "36"],
    colors: ["Blue", "Black", "Gray"],
    images: [
      "/placeholder.svg?height=600&width=600",
      "/placeholder.svg?height=600&width=600",
      "/placeholder.svg?height=600&width=600",
    ],
  },
  {
    id: 3,
    name: "Summer Floral Dress",
    price: 79.99,
    image: "/placeholder.svg?height=600&width=600",
    category: "women",
    isNew: true,
    description:
      "A lightweight floral dress perfect for summer days. Features a flattering silhouette with a flowy skirt and adjustable straps.",
    details: {
      material: "100% Viscose",
      fit: "Regular",
      care: "Hand wash cold, line dry",
      origin: "Made in India",
    },
    sizes: ["XS", "S", "M", "L", "XL"],
    colors: ["Floral Print", "Blue", "White"],
    images: [
      "/placeholder.svg?height=600&width=600",
      "/placeholder.svg?height=600&width=600",
      "/placeholder.svg?height=600&width=600",
    ],
  },
  {
    id: 4,
    name: "Casual Hoodie",
    price: 49.99,
    image: "/placeholder.svg?height=600&width=600",
    category: "men",
    isNew: false,
    description:
      "A comfortable casual hoodie perfect for everyday wear. Features a soft fleece lining and a relaxed fit for maximum comfort.",
    details: {
      material: "80% Cotton, 20% Polyester",
      fit: "Relaxed",
      care: "Machine wash cold, tumble dry low",
      origin: "Made in Vietnam",
    },
    sizes: ["S", "M", "L", "XL", "XXL"],
    colors: ["Gray", "Black", "Navy"],
    images: [
      "/placeholder.svg?height=600&width=600",
      "/placeholder.svg?height=600&width=600",
      "/placeholder.svg?height=600&width=600",
    ],
  },
]

export default function ProductPage({ params }: { params: { id: string } }) {
  const productId = Number.parseInt(params.id)
  const product = products.find((p) => p.id === productId)

  const [quantity, setQuantity] = useState(1)
  const [selectedSize, setSelectedSize] = useState("")
  const [selectedColor, setSelectedColor] = useState("")
  const [selectedImage, setSelectedImage] = useState(0)

  const { addToCart } = useCart()

  if (!product) {
    return (
      <div className="container px-4 py-12 mx-auto text-center">
        <h1 className="text-2xl font-bold">Product not found</h1>
        <p className="mt-4">The product you are looking for does not exist.</p>
        <Button asChild className="mt-6">
          <Link href="/products">Back to Products</Link>
        </Button>
      </div>
    )
  }

  const handleAddToCart = () => {
    if (!selectedSize || !selectedColor) return

    addToCart({
      ...product,
      quantity,
      //selectedSize,
      //selectedColor,
    })
  }

  return (
    <div className="container px-4 py-12 mx-auto">
      <div className="flex items-center gap-1 text-sm text-muted-foreground mb-8">
        <Link href="/" className="hover:text-foreground">
          Home
        </Link>
        <ChevronRight className="h-4 w-4" />
        <Link href="/products" className="hover:text-foreground">
          Products
        </Link>
        <ChevronRight className="h-4 w-4" />
        <span className="text-foreground">{product.name}</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
        <div className="space-y-4">
          <div className="relative aspect-square overflow-hidden rounded-lg border">
            <Image
              src={product.images[selectedImage] || "/placeholder.svg"}
              alt={product.name}
              fill
              className="object-cover"
            />
            {product.isNew && <Badge className="absolute top-4 right-4">New</Badge>}
          </div>

          <div className="flex gap-4">
            {product.images.map((image, index) => (
              <button
                key={index}
                className={`relative aspect-square w-20 overflow-hidden rounded-md border ${
                  selectedImage === index ? "ring-2 ring-primary" : ""
                }`}
                onClick={() => setSelectedImage(index)}
              >
                <Image
                  src={image || "/placeholder.svg"}
                  alt={`${product.name} - Image ${index + 1}`}
                  fill
                  className="object-cover"
                />
              </button>
            ))}
          </div>
        </div>

        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold">{product.name}</h1>
            <p className="text-2xl font-bold mt-2">${product.price.toFixed(2)}</p>
          </div>

          <p className="text-muted-foreground">{product.description}</p>

          <div className="space-y-4">
            <div>
              <h3 className="font-medium mb-2">Size</h3>
              <div className="flex flex-wrap gap-2">
                {product.sizes.map((size) => (
                  <Button
                    key={size}
                    variant={selectedSize === size ? "default" : "outline"}
                    className="min-w-[60px]"
                    onClick={() => setSelectedSize(size)}
                  >
                    {size}
                  </Button>
                ))}
              </div>
              {!selectedSize && <p className="text-sm text-muted-foreground mt-2">Please select a size</p>}
            </div>

            <div>
              <h3 className="font-medium mb-2">Color</h3>
              <div className="flex flex-wrap gap-2">
                {product.colors.map((color) => (
                  <Button
                    key={color}
                    variant={selectedColor === color ? "default" : "outline"}
                    className="min-w-[80px]"
                    onClick={() => setSelectedColor(color)}
                  >
                    {color}
                  </Button>
                ))}
              </div>
              {!selectedColor && <p className="text-sm text-muted-foreground mt-2">Please select a color</p>}
            </div>

            <div>
              <h3 className="font-medium mb-2">Quantity</h3>
              <div className="flex items-center">
                <Button variant="outline" size="icon" onClick={() => setQuantity(Math.max(1, quantity - 1))}>
                  <Minus className="h-4 w-4" />
                </Button>
                <span className="w-12 text-center">{quantity}</span>
                <Button variant="outline" size="icon" onClick={() => setQuantity(quantity + 1)}>
                  <Plus className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>

          <Button size="lg" className="w-full" disabled={!selectedSize || !selectedColor} onClick={handleAddToCart}>
            <ShoppingCart className="h-5 w-5 mr-2" />
            Add to Cart
          </Button>

          <Tabs defaultValue="details">
            <TabsList className="w-full">
              <TabsTrigger value="details" className="flex-1">
                Details
              </TabsTrigger>
              <TabsTrigger value="shipping" className="flex-1">
                Shipping & Returns
              </TabsTrigger>
            </TabsList>
            <TabsContent value="details" className="space-y-4 pt-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium">Material</h4>
                  <p className="text-sm text-muted-foreground">{product.details.material}</p>
                </div>
                <div>
                  <h4 className="font-medium">Fit</h4>
                  <p className="text-sm text-muted-foreground">{product.details.fit}</p>
                </div>
                <div>
                  <h4 className="font-medium">Care</h4>
                  <p className="text-sm text-muted-foreground">{product.details.care}</p>
                </div>
                <div>
                  <h4 className="font-medium">Origin</h4>
                  <p className="text-sm text-muted-foreground">{product.details.origin}</p>
                </div>
              </div>
            </TabsContent>
            <TabsContent value="shipping" className="space-y-4 pt-4">
              <div>
                <h4 className="font-medium">Shipping</h4>
                <p className="text-sm text-muted-foreground">
                  Free standard shipping on all orders over $100. Delivery within 3-5 business days.
                </p>
              </div>
              <div>
                <h4 className="font-medium">Returns</h4>
                <p className="text-sm text-muted-foreground">
                  We accept returns within 30 days of delivery. Items must be unworn, unwashed, and with the original
                  tags attached.
                </p>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  )
}

